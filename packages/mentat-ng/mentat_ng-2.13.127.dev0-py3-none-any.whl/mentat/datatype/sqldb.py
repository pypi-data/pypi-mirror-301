#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Datatype model library for PostgreSQL backend storages.

Overview
^^^^^^^^

The implementation is based on the great `sqlalchemy <http://www.sqlalchemy.org/>`__
library. This module provides models for following datatypes/objects:

:py:class:`mentat.datatype.sqldb.UserModel`
    Database representation of user account objects.

:py:class:`mentat.datatype.sqldb.GroupModel`
    Database representation of group objects.

:py:class:`mentat.datatype.sqldb.FilterModel`
    Database representation of group reporting filter objects.

:py:class:`mentat.datatype.sqldb.EventClassModel`
    Database representation of event class objects.

:py:class:`mentat.datatype.sqldb.NetworkModel`
    Database representation of network record objects for internal whois.

:py:class:`mentat.datatype.sqldb.SettingsReportingModel`
    Database representation of group settings objects.

:py:class:`mentat.datatype.sqldb.EventStatisticsModel`
    Database representation of event statistics objects.

:py:class:`mentat.datatype.sqldb.EventReportModel`
    Database representation of report objects.

:py:class:`mentat.datatype.sqldb.ItemChangeLogModel`
    Database representation of object changelog.

:py:class:`mentat.datatype.sqldb.DetectorModel`
    Database representation of detector objects.

.. warning::

    Current implementation is for optimalization purposes using some advanced
    features provided by the `PostgreSQL <https://www.postgresql.org/>`__
    database and no other engines are currently supported.

"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import datetime
import difflib
import json
import random
import string

import sqlalchemy
import sqlalchemy.dialects.postgresql
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from sqlalchemy.schema import DropTable
import sqlalchemy.types
from werkzeug.security import check_password_hash, generate_password_hash

import mentat.const
from mentat.const import (
    REPORT_SEVERITIES,
    REPORT_TYPES,
    REPORTING_FILTER_BASIC,
    REPORTING_FILTERS,
    REPORTING_MODES
)


#
# Modify compilation of DROP TABLE for PostgreSQL databases to enable CASCADE feature.
# Otherwise it is not possible to delete the database schema with:
#   MODEL.metadata.drop_all(engine)
#
@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):  # pylint: disable=locally-disabled,unused-argument
    return compiler.visit_drop_table(element) + " CASCADE"


#-------------------------------------------------------------------------------


class MODEL:
    """
    Base class for all `sqlalchemy <http://www.sqlalchemy.org/>`__ database models
    and providing the `declarative base <http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declarative_base>`__.
    All required database objects should be implemented by extending this base model.
    """
    @declared_attr
    def id(self):  # pylint: disable=locally-disabled,invalid-name
        """
        Common table column for unique numeric identifier, implementation is based
        on `declared_attr <http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declared_attr>`__
        pattern.
        """
        return sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)

    @declared_attr
    def createtime(self):
        """
        Common table column for object creation timestamps, implementation is based
        on `declared_attr <http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declared_attr>`__
        pattern.
        """
        return sqlalchemy.Column(sqlalchemy.DateTime, default = datetime.datetime.utcnow)

    def get_id(self):
        """
        Getter for retrieving current ID.
        """
        return self.id

    def to_dict(self):
        """
        Export object into dictionary containing only primitive data types.
        """
        raise NotImplementedError()

    def to_json(self):
        """
        Export object into JSON string.
        """
        return json.dumps(self.to_dict(), indent = 4, sort_keys = True)


MODEL = declarative_base(cls = MODEL)


_asoc_group_members = sqlalchemy.Table(  # pylint: disable=locally-disabled,invalid-name
    'asoc_group_members',
    MODEL.metadata,
    sqlalchemy.Column('group_id', sqlalchemy.ForeignKey('groups.id'), primary_key = True),
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id'), primary_key = True),
)
"""
Association table representing user*group relation: group membership.

What users are members of what groups.
"""

_asoc_group_members_wanted = sqlalchemy.Table(  # pylint: disable=locally-disabled,invalid-name
    'asoc_group_members_wanted',
    MODEL.metadata,
    sqlalchemy.Column('group_id', sqlalchemy.ForeignKey('groups.id'), primary_key = True),
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id'), primary_key = True),
)
"""
Association table representing user*group relation: wanted group membership.

What users want to be members of what groups.
"""

_asoc_group_managers = sqlalchemy.Table(  # pylint: disable=locally-disabled,invalid-name
    'asoc_group_managers',
    MODEL.metadata,
    sqlalchemy.Column('group_id', sqlalchemy.ForeignKey('groups.id'), primary_key = True),
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey('users.id'), primary_key = True),
)
"""
Association table representing user*group relation: group management.

What users can manage what groups.
"""

_asoc_groups_reports = sqlalchemy.Table(  # pylint: disable=locally-disabled,invalid-name
    'asoc_groups_reports',
    MODEL.metadata,
    sqlalchemy.Column('group_id', sqlalchemy.ForeignKey('groups.id', onupdate = "CASCADE", ondelete = "CASCADE"), primary_key = True),
    sqlalchemy.Column('report_id', sqlalchemy.ForeignKey('reports_events.id', onupdate = "CASCADE", ondelete = "CASCADE"), primary_key = True),
)
"""
Association table representing group*report relation: ownership of report.

What reports are linked to what groups (n:m relationship).
"""


class UserModel(MODEL):
    """
    Class representing user objects within the SQL database mapped to ``users``
    table.
    """
    __tablename__ = 'users'

    login        = sqlalchemy.Column(sqlalchemy.String(50), sqlalchemy.CheckConstraint('login = lower(login)', name='login_lowercase'), unique = True, index = True)
    fullname     = sqlalchemy.Column(sqlalchemy.String(100), nullable = False)
    email        = sqlalchemy.Column(sqlalchemy.String(250), sqlalchemy.CheckConstraint('email = lower(email)', name='email_lowercase'), nullable = False)
    organization = sqlalchemy.Column(sqlalchemy.String(250), nullable = False)
    roles        = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String(20), dimensions = 1), nullable = False, default = [])
    password     = sqlalchemy.Column(sqlalchemy.String)
    apikey       = sqlalchemy.Column(sqlalchemy.String, unique = True, index = True)
    enabled      = sqlalchemy.Column(sqlalchemy.Boolean, nullable = False, default = True)

    locale     = sqlalchemy.Column(sqlalchemy.String(20))
    timezone   = sqlalchemy.Column(sqlalchemy.String(50))

    memberships = sqlalchemy.orm.relationship('GroupModel', secondary = _asoc_group_members, back_populates = 'members', order_by = 'GroupModel.name')
    memberships_wanted = sqlalchemy.orm.relationship('GroupModel', secondary = _asoc_group_members_wanted, back_populates = 'members_wanted', order_by = 'GroupModel.name')
    managements = sqlalchemy.orm.relationship('GroupModel', secondary = _asoc_group_managers, back_populates = 'managers', order_by = 'GroupModel.name')

    changelogs  = sqlalchemy.orm.relationship('ItemChangeLogModel', back_populates = 'author', order_by = 'ItemChangeLogModel.createtime')

    logintime  = sqlalchemy.Column(sqlalchemy.DateTime)

    def __repr__(self):
        return "<User(login='%s', fullname='%s')>" % (self.login, self.fullname)

    def __str__(self):
        return '{}'.format(self.login)

    @validates('login', 'email')
    def convert_lower(self, key, value):  # pylint: disable=locally-disabled,unused-argument
        """
        Convert login and email to lowercase.
        """
        return value.lower()

    def is_state_enabled(self):
        """
        Check if current user account state is enabled.
        """
        return self.enabled

    def is_state_disabled(self):
        """
        Check if current user account state is disabled.
        """
        return not self.enabled

    def set_state_enabled(self):
        """
        Set current user account state to enabled.
        """
        self.enabled = True

    def set_state_disabled(self):
        """
        Set current user account state to disabled.
        """
        self.enabled = False

    def set_password(self, password_plain):
        """
        Generate and set password hash from given plain text password.
        """
        self.password = generate_password_hash(password_plain)

    def check_password(self, password_plain):
        """
        Check given plaintext password agains internal password hash.
        """
        return check_password_hash(self.password, password_plain)

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.datatype.sqldb.MODEL.to_dict` method.
        """
        return {
            'id':                 self.id,
            'createtime':         str(self.createtime),
            'logintime':          str(self.logintime),
            'login':              self.login,
            'fullname':           self.fullname,
            'email':              self.email,
            'organization':       self.organization,
            'roles':              [ str(x) for x in self.roles],
            'apikey':             self.apikey,
            'password':           self.password,
            'enabled':            bool(self.enabled),
            'locale':             self.locale,
            'timezone':           self.timezone,
            'memberships':        [(x.id, x.name) for x in self.memberships],
            'memberships_wanted': [(x.id, x.name) for x in self.memberships_wanted],
            'managements':        [(x.id, x.name) for x in self.managements]
        }

    #---------------------------------------------------------------------------
    # Custom methods for Hawat user interface. Just couple of methods required by
    # the flask_login extension.
    #---------------------------------------------------------------------------

    @property
    def is_authenticated(self):
        """
        Mandatory interface required by the :py:mod:`flask_login` extension.
        """
        return True

    @property
    def is_active(self):
        """
        Mandatory interface required by the :py:mod:`flask_login` extension.
        """
        return self.enabled

    @property
    def is_anonymous(self):
        """
        Mandatory interface required by the :py:mod:`flask_login` extension.
        """
        return False

    def get_id(self):
        """
        Mandatory interface required by the :py:mod:`flask_login` extension.
        """
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def has_role(self, role):
        """
        Returns ``True`` if the user identifies with the specified role.

        :param str role: A role name.
        """
        return role in self.roles

    def has_no_role(self):
        """
        Returns ``True`` if the user has no role.
        """
        return len(self.roles) == 0


def usermodel_from_typeddict(structure, defaults = None):
    """
    Convenience method for creating :py:class:`mentat.datatype.sqldb.UserModel`
    object from :py:class:`mentat.datatype.internal.User` objects.
    """
    if not defaults:
        defaults = {}

    sqlobj = UserModel()
    sqlobj.login        = structure.get('_id')
    sqlobj.createtime   = structure.get('ts')  # pylint: disable=locally-disabled,attribute-defined-outside-init
    sqlobj.fullname     = structure.get('name')
    sqlobj.email        = structure.get('email', structure.get('_id'))
    sqlobj.organization = structure.get('organization')
    sqlobj.roles        = [str(i) for i in structure.get('roles', [])]
    sqlobj.enabled      = 'user' in sqlobj.roles

    return sqlobj


class GroupModel(MODEL):
    """
    Class representing group objects within the SQL database mapped to ``groups``
    table.
    """
    __tablename__ = 'groups'

    name        = sqlalchemy.Column(sqlalchemy.String(100), unique = True, index = True)
    source      = sqlalchemy.Column(sqlalchemy.String(50), nullable = False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    enabled     = sqlalchemy.Column(sqlalchemy.Boolean, nullable = False, default = True)

    members = sqlalchemy.orm.relationship('UserModel', secondary = _asoc_group_members, back_populates = 'memberships', order_by = 'UserModel.fullname')
    members_wanted = sqlalchemy.orm.relationship('UserModel', secondary = _asoc_group_members_wanted, back_populates = 'memberships_wanted', order_by = 'UserModel.fullname')
    managers = sqlalchemy.orm.relationship('UserModel', secondary = _asoc_group_managers, back_populates = 'managements', order_by = 'UserModel.fullname')

    networks = sqlalchemy.orm.relationship('NetworkModel', back_populates = 'group', cascade = 'all, delete-orphan', order_by = 'NetworkModel.netname')
    filters  = sqlalchemy.orm.relationship('FilterModel', back_populates = 'group', cascade = 'all, delete-orphan', order_by = 'FilterModel.name')
    reports  = sqlalchemy.orm.relationship('EventReportModel', secondary = _asoc_groups_reports, back_populates = 'groups', order_by = 'EventReportModel.label')

    settings_rep = sqlalchemy.orm.relationship('SettingsReportingModel', uselist = False, back_populates = 'group', cascade = 'all, delete-orphan')

    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id'))
    children  = sqlalchemy.orm.relationship('GroupModel', backref = sqlalchemy.orm.backref('parent', remote_side='GroupModel.id'))

    local_id = sqlalchemy.Column(sqlalchemy.String(20))

    def __repr__(self):
        return "<Group(name='%s')>" % (self.name)

    def __str__(self):
        return '{}'.format(self.name)

    def is_state_enabled(self):
        """
        Check if current group state is enabled.
        """
        return self.enabled

    def is_state_disabled(self):
        """
        Check if current group state is disabled.
        """
        return not self.enabled

    def set_state_enabled(self):
        """
        Set current group state to enabled.
        """
        self.enabled = True

    def set_state_disabled(self):
        """
        Set current group state to disabled.
        """
        self.enabled = False

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.datatype.sqldb.MODEL.to_dict` method.
        """
        return {
            'id':             int(self.id),
            'createtime':     str(self.createtime),
            'name':           str(self.name),
            'source':         str(self.source),
            'description':    str(self.description),
            'enabled':        bool(self.enabled),
            'members':        [(x.id, x.login) for x in self.members],
            'members_wanted': [(x.id, x.login) for x in self.members_wanted],
            'managers':       [(x.id, x.login) for x in self.managers],
            'networks':       [(x.id, x.network) for x in self.networks],
            'filters':        [(x.id, x.filter) for x in self.filters],
            'parent':         str(self.parent),
            'local_id':       str(self.local_id)
        }


@sqlalchemy.event.listens_for(GroupModel.members, 'append')
def enforce_wanted_memberships_consistency(group, user, initiator):
    """
    This event method is triggered if user is added to members of group, and it enforces
    consistency by removing him from members_wanted (if present).
    """
    try:
        group.members_wanted.remove(user)
    except ValueError:
        pass


def groupmodel_from_typeddict(structure, defaults = None):
    """
    Convenience method for creating :py:class:`mentat.datatype.sqldb.GroupModel`
    object from :py:class:`mentat.datatype.internal.AbuseGroup` objects.
    """
    if not defaults:
        defaults = {}

    sqlobj = GroupModel()
    sqlobj.name        = structure.get('_id')
    sqlobj.source      = structure.get('source')
    sqlobj.description = structure.get('description', defaults.get('netname', '-- undisclosed --'))
    sqlobj.createtime  = structure.get('ts')  # pylint: disable=locally-disabled,attribute-defined-outside-init
    sqlobj.local_id    = structure.get('local_id', None)

    return sqlobj


class iprange(sqlalchemy.types.UserDefinedType):
    cache_ok = True

    def get_col_spec(self, **kw):
        return "iprange"

    def bind_processor(self, dialect):
        def process(value):
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value
        return process


class NetworkModel(MODEL):
    """
    Class representing network records objects within the SQL database mapped to
    ``networks`` table.
    """
    __tablename__ = 'networks'

    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id', onupdate = "CASCADE", ondelete = "CASCADE"), nullable = False)
    group    = sqlalchemy.orm.relationship('GroupModel', back_populates = 'networks')

    netname     = sqlalchemy.Column(sqlalchemy.String(250), nullable = False)
    source      = sqlalchemy.Column(sqlalchemy.String(50), nullable = False)
    network     = sqlalchemy.Column(iprange, nullable = False)
    description = sqlalchemy.Column(sqlalchemy.String)
    rank        = sqlalchemy.Column(sqlalchemy.Integer)
    is_base     = sqlalchemy.Column(sqlalchemy.Boolean, nullable = False, default = False)
    local_id    = sqlalchemy.Column(sqlalchemy.String(20))

    def __repr__(self):
        return "<Network(netname='%s',network='%s')>" % (self.netname, self.network)

    def __str__(self):
        return '{}'.format(self.netname)

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.datatype.sqldb.MODEL.to_dict` method.
        """
        return {
            'id':          int(self.id),
            'createtime':  str(self.createtime),
            'group':       str(self.group),
            'netname':     str(self.netname),
            'source':      str(self.source),
            'network':     str(self.network),
            'description': str(self.description),
            'rank':        int(self.rank) if self.rank else None,
            'is_base':     bool(self.is_base),
            'local_id':    str(self.local_id)
        }


def networkmodel_from_typeddict(structure, defaults = None):
    """
    Convenience method for creating :py:class:`mentat.datatype.sqldb.NetworkModel`
    object from :py:class:`mentat.datatype.internal.NetworkRecord` objects.
    """
    if not defaults:
        defaults = {}

    sqlobj = NetworkModel()
    sqlobj.network     = structure.get('network')
    sqlobj.source      = structure.get('source')
    sqlobj.netname     = structure.get('netname', defaults.get('netname', '-- undisclosed --'))
    sqlobj.description = structure.get('description', defaults.get('description', None))
    sqlobj.rank        = structure.get('rank', None)
    sqlobj.is_base     = bool(structure.get('is_base', False))
    sqlobj.local_id    = structure.get('local_id', None)

    return sqlobj


class FilterModel(MODEL):  # pylint: disable=locally-disabled,too-many-instance-attributes
    """
    Class representing reporting filters objects within the SQL database mapped to
    ``filters`` table.
    """
    __tablename__ = 'filters'

    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id', onupdate = "CASCADE", ondelete = "CASCADE"), nullable = False)
    group    = sqlalchemy.orm.relationship('GroupModel', back_populates = 'filters')

    name          = sqlalchemy.Column(sqlalchemy.String(250), nullable = False)
    source_based  = sqlalchemy.Column(sqlalchemy.Boolean, default = True, nullable = False)
    type          = sqlalchemy.Column(sqlalchemy.Enum(*REPORTING_FILTERS, name='filter_types'), default = REPORTING_FILTER_BASIC, nullable = False)
    filter        = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    description   = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    valid_from    = sqlalchemy.Column(sqlalchemy.DateTime)
    valid_to      = sqlalchemy.Column(sqlalchemy.DateTime)
    enabled       = sqlalchemy.Column(sqlalchemy.Boolean, default = False, nullable = False)
    detectors     = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions = 1), default = [], nullable = False)
    categories    = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions = 1), default = [], nullable = False)
    event_classes = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions=1), default=[], nullable=False)
    sources       = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions = 1), default = [], nullable = False)
    targets       = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions=1), default=[], nullable=False)
    protocols     = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions=1), default=[], nullable=False)
    hits          = sqlalchemy.Column(sqlalchemy.Integer, default = 0, nullable = False)
    last_hit      = sqlalchemy.Column(sqlalchemy.DateTime)

    def __repr__(self):
        return "<Filter(name='%s')>" % (self.name)

    def __str__(self):
        return '{}'.format(self.name)

    def is_state_enabled(self):
        """
        Check if current filter state is enabled.
        """
        return self.enabled

    def is_state_disabled(self):
        """
        Check if current filter state is disabled.
        """
        return not self.enabled

    def set_state_enabled(self):
        """
        Set current filter state to enabled.
        """
        self.enabled = True

    def set_state_disabled(self):
        """
        Set current filter state to disabled.
        """
        self.enabled = False

    @hybrid_property
    def is_expired(self):
        """
        Returns True if the filter already expired, False otherwise.
        """
        return self.valid_to is not None and self.valid_to < datetime.datetime.utcnow()

    @hybrid_property
    def will_be_valid(self):
        """
        Returns True if the filter is not valid now, but has a future validity.
        Returns False otherwise.
        """
        return self.valid_from is not None and self.valid_from > datetime.datetime.utcnow()

    @property
    def is_valid(self):
        """
        Returns True if the filter is valid, False otherwise.
        """
        return not self.will_be_valid and not self.is_expired

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.datatype.sqldb.MODEL.to_dict` method.
        """
        return {
            'id':            int(self.id),
            'createtime':    str(self.createtime),
            'group':         str(self.group),
            'name':          str(self.name),
            'source_based':  str(self.source_based),
            'type':          str(self.type),
            'filter':        str(self.filter),
            'description':   str(self.description),
            'valid_from':    str(self.valid_from),
            'valid_to':      str(self.valid_to),
            'enabled':       bool(self.enabled),
            'detectors':     [str(x) for x in self.detectors],
            'categories':    [str(x) for x in self.categories],
            'event_classes': [str(x) for x in self.event_classes],
            'sources':       [str(x) for x in self.sources],
            'targets':       [str(x) for x in self.targets],
            'protocols':     [str(x) for x in self.protocols],
            'hits':          int(self.hits),
            'last_hit':      str(self.last_hit)
        }


def filtermodel_from_typeddict(structure, defaults = None):
    """
    Convenience method for creating :py:class:`mentat.datatype.sqldb.NetworkModel`
    object from :py:class:`mentat.datatype.internal.NetworkRecord` objects.
    """
    if not defaults:
        defaults = {}

    sqlobj = FilterModel()

    sqlobj.name        = structure.get('_id')
    sqlobj.createtime  = structure.get('ts')  # pylint: disable=locally-disabled,attribute-defined-outside-init
    sqlobj.type        = structure.get('type')
    sqlobj.filter      = structure.get('filter')
    sqlobj.description = structure.get('description') + structure.get('note', '')
    sqlobj.valid_from  = structure.get('validfrom', None)
    sqlobj.valid_to    = structure.get('validto', None)
    sqlobj.enabled     = bool(structure.get('enabled', False))
    sqlobj.detectors   = structure.get('analyzers', [])
    sqlobj.categories  = structure.get('categories', [])
    sqlobj.sources     = structure.get('ips', [])
    sqlobj.hits        = structure.get('hits', 0)
    sqlobj.last_hit    = structure.get('lasthit', None)

    return sqlobj


class EventClassModel(MODEL):  # pylint: disable=locally-disabled,too-many-instance-attributes
    """
    Class representing event class objects within the SQL database mapped to
    ``event_classes`` table.
    """
    __tablename__ = 'event_classes'

    name             = sqlalchemy.Column(sqlalchemy.String(250), unique = True, nullable = False)
    source_based     = sqlalchemy.Column(sqlalchemy.Boolean, default=True, nullable=False)
    label_en         = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    label_cz         = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    reference        = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    displayed_main   = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions=1), default=[], nullable=False)
    displayed_source = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions=1), default=[], nullable=False)
    displayed_target = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions=1), default=[], nullable=False)

    rule        = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    severity    = sqlalchemy.Column(sqlalchemy.Enum(*REPORT_SEVERITIES, name='event_class_severities'), nullable=False)
    subclassing = sqlalchemy.Column(sqlalchemy.String, nullable = True)

    enabled     = sqlalchemy.Column(sqlalchemy.Boolean, default = False, nullable = False)

    last_update = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, index=True)

    def __repr__(self):
        return "<EventClass(name='%s')>" % (self.name)

    def __str__(self):
        return '{}'.format(self.name)

    def is_state_enabled(self):
        """
        Check if current event class state is enabled.
        """
        return self.enabled

    def is_state_disabled(self):
        """
        Check if current event class state is disabled.
        """
        return not self.enabled

    def set_state_enabled(self):
        """
        Set current event class state to enabled.
        """
        self.enabled = True

    def set_state_disabled(self):
        """
        Set current event class state to disabled.
        """
        self.enabled = False

    def is_source_based(self):
        """
        Returns if the event class is source-based.
        """
        return self.source_based

    def is_target_based(self):
        """
        Returns if the event class is target-based.
        If it is not source based, it is target based.
        """
        return not self.source_based

    def get_type(self):
        """
        Returns the type of this event class as a string.
        """
        return 'Source-based' if self.is_source_based() else 'Target-based'

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.datatype.sqldb.MODEL.to_dict` method.
        """
        return {
            'id':               int(self.id),
            'name':             str(self.name),
            'type':             self.get_type(),
            'label_en':         str(self.label_en),
            'label_cz':         str(self.label_cz),
            'reference':        str(self.reference),
            'displayed_main':   [str(x) for x in self.displayed_main],
            'displayed_source': [str(x) for x in self.displayed_source],
            'displayed_target': [str(x) for x in self.displayed_target],
            'rule':             str(self.rule),
            'severity':         str(self.severity),
            'subclassing':      str(self.subclassing),
            'enabled':          bool(self.enabled)
        }

    def get_inspection_subclass_rule(self):
        """
        If subclassing is enabled, return derived inspection rule
        for setting the subclass of the evnet accordingly.
        If subclassing is disabled, return None.
        """
        if self.subclassing is None or not self.subclassing:
            return None
        return {
            "name": f"Assign subclass for class {self.name}",
            "rule": self.rule,
            "actions": [
                {
                    "action": "set",
                    "args": {
                        "path": f"_Mentat.{'Target' if self.is_target_based() else 'Event'}Subclass",
                        "expression": self.subclassing,
                        "unique": True
                    }
                }
            ]
        }

    def get_inspection_rules(self):
        """
        Returns inspection rules derived from attributes of the event class
        object. This can then be used in mentat-inspector module.
        """
        rules = [
            {
                "name": f"Assign class - {self.name}",
                "rule": self.rule,
                "actions": [
                    {
                        "action": "tag",
                        "args": {
                            "path": f"_Mentat.{'Target' if self.is_target_based() else 'Event'}Class",
                            "value": self.name,
                            "overwrite": False
                        }
                    },
                    {
                        "action": "tag",
                        "args": {
                            "path": f"_Mentat.{'Target' if self.is_target_based() else 'Event'}Severity",
                            "value": self.severity,
                            "overwrite": False
                        }
                    }
                ]
            }
        ]
        # If subclassing is enabled, add the subclass rule too.
        if self.get_inspection_subclass_rule() is not None:
            rules.append(self.get_inspection_subclass_rule())
        return rules

    def should_be_displayed(self, field_type, field_name):
        """
        Checks if field_name (e.g. "port") from the given field_type (e.g. "source")
        should be displayed according to event_class settings.
        """
        if field_type.lower() == "source":
            return field_name in self.displayed_source
        if field_type.lower() == "target":
            return field_name in self.displayed_target
        return field_name in self.displayed_main


class SettingsReportingModel(MODEL):  # pylint: disable=locally-disabled,too-few-public-methods
    """
    Class representing reporting settings objects within the SQL database mapped to
    ``settings_reporting`` table.
    """
    __tablename__ = 'settings_reporting'

    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id', onupdate = "CASCADE", ondelete = "CASCADE"), nullable = False)
    group = sqlalchemy.orm.relationship('GroupModel', back_populates = 'settings_rep')

    emails_low = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions = 1), default = [], nullable = False)
    emails_medium = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions = 1), default = [], nullable = False)
    emails_high = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions = 1), default = [], nullable = False)
    emails_critical = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions = 1), default = [], nullable = False)
    mode = sqlalchemy.Column(sqlalchemy.Enum(*REPORTING_MODES, name='reporting_modes'))
    locale = sqlalchemy.Column(sqlalchemy.String)
    timezone = sqlalchemy.Column(sqlalchemy.String)

    redirect = sqlalchemy.Column(sqlalchemy.Boolean)

    def __repr__(self):
        return "<SettingsReporting(id='%d',group_id='%d')>" % (int(self.id), int(self.group_id))

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.datatype.sqldb.MODEL.to_dict` method.
        """
        return {
            'id':                 int(self.id),
            'createtime':         str(self.createtime),
            'group':              str(self.group),
            'emails_low':         [str(x) for x in self.emails_low],
            'emails_medium':      [str(x) for x in self.emails_medium],
            'emails_high':        [str(x) for x in self.emails_high],
            'emails_critical':    [str(x) for x in self.emails_critical],
            'mode':               str(self.mode) if self.mode is not None else None,
            'locale':             str(self.locale) if self.locale is not None else None,
            'timezone':           str(self.timezone) if self.timezone is not None else None,
            'redirect':           bool(self.redirect) if self.redirect is not None else None
        }


def setrepmodel_from_typeddict(structure, defaults = None):
    """
    Convenience method for creating :py:class:`mentat.datatype.sqldb.SettingsReportingModel`
    object from :py:class:`mentat.datatype.internal.AbuseGroup` objects.
    """
    if not defaults:
        defaults = {}

    sqlobj = SettingsReportingModel()
    sqlobj.emails_low         = structure.get('rep_emails_low', [])
    sqlobj.emails_medium      = structure.get('rep_emails_medium', [])
    sqlobj.emails_high        = structure.get('rep_emails_high', [])
    sqlobj.emails_critical    = structure.get('rep_emails_critical', [])
    sqlobj.mode               = structure.get('rep_mode', None)
    sqlobj.redirect           = structure.get('rep_redirect', None)

    if sqlobj.emails and '@' not in sqlobj.emails[0]:
        sqlobj.emails = [''.join(sqlobj.emails)]

    return sqlobj


class EventStatisticsModel(MODEL):  # pylint: disable=locally-disabled,too-many-instance-attributes
    """
    Class representing event statistics objects within the SQL database mapped to
    ``statistics_events`` table.
    """
    __tablename__ = 'statistics_events'

    interval       = sqlalchemy.Column(sqlalchemy.String, nullable = False, unique = True, index = True)
    dt_from        = sqlalchemy.Column(sqlalchemy.DateTime, nullable = False)
    dt_to          = sqlalchemy.Column(sqlalchemy.DateTime, nullable = False)
    delta          = sqlalchemy.Column(sqlalchemy.Integer, nullable = False)
    count          = sqlalchemy.Column(sqlalchemy.Integer, nullable = False)
    stats_overall  = sqlalchemy.Column(sqlalchemy.dialects.postgresql.JSONB(none_as_null = True))
    stats_internal = sqlalchemy.Column(sqlalchemy.dialects.postgresql.JSONB(none_as_null = True))
    stats_external = sqlalchemy.Column(sqlalchemy.dialects.postgresql.JSONB(none_as_null = True))

    def __repr__(self):
        return "<EventStatistics(interval='%s',delta='%d')>" % (self.interval, self.delta)

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.datatype.sqldb.MODEL.to_dict` method.
        """
        return {
            'id':             int(self.id),
            'createtime':     str(self.createtime),
            'interval':       str(self.interval),
            'dt_from':        str(self.dt_from),
            'dt_to':          str(self.dt_to),
            'delta':          int(self.delta),
            'count':          int(self.count),
            'stats_overall':  self.stats_overall,
            'stats_internal': self.stats_internal,
            'stats_external': self.stats_external
        }

    @staticmethod
    def format_interval(dtl, dth):
        """
        Format two given timestamps into single string desribing the interval
        between them. This string can be then used as a form of a label.

        :param datetime.datetime dtl: Lower interval boundary.
        :param datetime.datetime dth: Upper interval boundary.
        :return: Interval between timestamps.
        :rtype: str
        """
        return '{}_{}'.format(dtl.strftime('%FT%T'), dth.strftime('%FT%T'))

    def calculate_interval(self):
        """
        Calculate and set internal interval label.
        """
        self.interval = self.format_interval(self.dt_from, self.dt_to)

    def calculate_delta(self):
        """
        Calculate and set delta between internal time interval boundaries.
        """
        delta = self.dt_to - self.dt_from
        self.delta = delta.total_seconds()


def eventstatsmodel_from_typeddict(structure, defaults = None):
    """
    Convenience method for creating :py:class:`mentat.datatype.sqldb.EventStatisticsModel`
    object from :py:class:`mentat.datatype.internal.EventStat` objects.
    """
    if not defaults:
        defaults = {}

    interval = '{}_{}'.format(structure['ts_from'].strftime('%FT%T'), structure['ts_to'].strftime('%FT%T'))
    delta = structure['ts_to'] - structure['ts_from']

    sqlobj = EventStatisticsModel()
    sqlobj.interval       = interval
    sqlobj.createtime     = structure['ts']  # pylint: disable=locally-disabled,attribute-defined-outside-init
    sqlobj.dt_from        = structure['ts_from']
    sqlobj.dt_to          = structure['ts_to']
    sqlobj.delta          = delta.total_seconds()
    sqlobj.count          = structure.get('count', structure['overall'].get('cnt_alerts'))
    sqlobj.stats_overall  = structure['overall']
    sqlobj.stats_internal = structure.get('internal', dict())   # pylint: disable=locally-disabled,use-dict-literal
    sqlobj.stats_external = structure.get('external', dict())   # pylint: disable=locally-disabled,use-dict-literal

    return sqlobj


class ReportStatisticsJSONB(sqlalchemy.types.TypeDecorator):
    """
    Class representing a JSONB type used for report statistics in order to
    ensure compatibility with legacy reports.
    """
    impl = sqlalchemy.dialects.postgresql.JSONB

    cache_ok = True

    def process_result_value(self, value, dialect):  # pylint: disable=locally-disabled,unused-argument
        """
        Rename 'ips' to 'sources'
        """
        if not isinstance(value, dict):
            return value
        if 'ips' in value and 'sources' not in value:
            value['sources'] = value.pop('ips')
        return value

    def coerce_compared_value(self, op, value):
        """
        Ensure proper coersion
        """
        return self.impl.coerce_compared_value(op, value)


class EventReportModel(MODEL):
    """
    Class representing event report objects within the SQL database mapped to
    ``reports_events`` table.
    """
    __tablename__ = 'reports_events'

    #group_name = sqlalchemy.Column(sqlalchemy.String, nullable = False, index = True)
    groups    = sqlalchemy.orm.relationship('GroupModel', secondary = _asoc_groups_reports, back_populates = 'reports')

    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('reports_events.id'))
    children  = sqlalchemy.orm.relationship('EventReportModel', backref = sqlalchemy.orm.backref('parent', remote_side='EventReportModel.id'))

    label    = sqlalchemy.Column(sqlalchemy.String, nullable = False, unique = True, index = True)
    severity = sqlalchemy.Column(sqlalchemy.Enum(*REPORT_SEVERITIES, name='report_severities'), nullable = False)
    type     = sqlalchemy.Column(sqlalchemy.Enum(*REPORT_TYPES, name='report_types'), nullable = False)
    message  = sqlalchemy.Column(sqlalchemy.String)

    dt_from = sqlalchemy.Column(sqlalchemy.DateTime, nullable = False)
    dt_to   = sqlalchemy.Column(sqlalchemy.DateTime, nullable = False)
    delta   = sqlalchemy.Column(sqlalchemy.Integer, nullable = False)

    flag_testdata = sqlalchemy.Column(sqlalchemy.Boolean, default = False, nullable = False)
    flag_mailed   = sqlalchemy.Column(sqlalchemy.Boolean, default = False, nullable = False)

    # Number of events actually in report (evcount_thr + evcount_rlp).
    evcount_rep     = sqlalchemy.Column(sqlalchemy.Integer, nullable = False)
    # Initial number of events for reporting (evcount_new + evcount_rlp).
    evcount_all     = sqlalchemy.Column(sqlalchemy.Integer, nullable = False)
    # Number of matching events fetched from database.
    evcount_new     = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of events remaining after filtering.
    evcount_flt     = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of events blocked by filters (evcount_new - evcount_flt).
    evcount_flt_blk = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of events remaining after filtering by detectors credibility.
    evcount_det     = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of events coming from uncredible detectors (evcount_flt - evcount_dlt).
    evcount_det_blk = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of events remaining after thresholding.
    evcount_thr     = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of events blocked by thresholds (evcount_dlt - evcount_thr).
    evcount_thr_blk = sqlalchemy.Column(sqlalchemy.Integer)
    # Number of relapsed events.
    evcount_rlp     = sqlalchemy.Column(sqlalchemy.Integer)

    mail_to  = sqlalchemy.Column(sqlalchemy.dialects.postgresql.ARRAY(sqlalchemy.String, dimensions = 1), default = [], nullable = False)
    mail_dt  = sqlalchemy.Column(sqlalchemy.DateTime)
    mail_res = sqlalchemy.Column(sqlalchemy.String)

    statistics = sqlalchemy.Column(ReportStatisticsJSONB(none_as_null = True))
    filtering  = sqlalchemy.Column(sqlalchemy.dialects.postgresql.JSONB(none_as_null = True))
    structured_data = sqlalchemy.Column(sqlalchemy.dialects.postgresql.JSONB(none_as_null=True))

    def __repr__(self):
        return "<EventReport(label='%s')>" % (self.label)

    def __str__(self):
        return '{}'.format(self.label)

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.datatype.sqldb.MODEL.to_dict` method.
        """
        return {
            'id':              int(self.id),
            'createtime':      str(self.createtime),
            'groups':          [str(group) for group in self.groups],
            'parent':          str(self.parent),
            'label':           str(self.label),
            'severity':        str(self.severity),
            'type':            str(self.type),
            'message':         str(self.message),
            'dt_from':         str(self.dt_from),
            'dt_to':           str(self.dt_to),
            'delta':           str(self.delta),
            'flag_testdata':   bool(self.flag_testdata),
            'flag_mailed':     bool(self.flag_mailed),
            'evcount_rep':     int(self.evcount_rep) if self.evcount_rep else 0,
            'evcount_all':     int(self.evcount_all) if self.evcount_all else 0,
            'evcount_new':     int(self.evcount_new) if self.evcount_new else 0,
            'evcount_flt':     int(self.evcount_flt) if self.evcount_flt else 0,
            'evcount_flt_blk': int(self.evcount_flt_blk) if self.evcount_flt_blk else 0,
            'evcount_det':     int(self.evcount_det) if self.evcount_det else 0,
            'evcount_det_blk': int(self.evcount_det_blk) if self.evcount_det_blk else 0,
            'evcount_thr':     int(self.evcount_thr) if self.evcount_thr else 0,
            'evcount_thr_blk': int(self.evcount_thr_blk) if self.evcount_thr_blk else 0,
            'evcount_rlp':     int(self.evcount_rlp) if self.evcount_rlp else 0,
            'mail_to':         str(self.mail_to),
            'mail_dt':         str(self.mail_dt),
            'mail_res':        str(self.mail_res),
            'statistics':      str(self.statistics),
            'filtering':       str(self.filtering),
            'structured_data': str(self.structured_data),
        }

    def to_dict_short(self):
        """
        Returns shortened version of to_dict method. Used for debugging.
        """
        dictionary = self.to_dict()
        dictionary.pop("statistics")
        dictionary.pop("structured_data")
        dictionary.pop("filtering")
        return dictionary

    def calculate_delta(self):
        """
        Calculate delta between internal time interval boundaries.
        """
        delta = self.dt_to - self.dt_from
        self.delta = delta.total_seconds()
        return self.delta

    def generate_label(self):
        """
        Generate and set label from internal attributes.
        """
        dt_cur = datetime.datetime.utcnow()
        self.label = 'M{:4d}{:02d}{:02d}{:1s}{:1s}-{:5s}'.format(
            dt_cur.year,
            dt_cur.month,
            dt_cur.day,
            self.type[0].upper(),
            self.severity[0].upper(),
            ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
        )
        return self.label

    def is_old_type(self):
        """
        Returns True if the report has an old type of structured data.
        (structured data which is not sorted according to detectors)
        """
        if not self.structured_data:
            return True
        if self.type == mentat.const.REPORT_TYPE_TARGET:
            return False
        for section in ['regular', 'relapsed']:
            if self.structured_data[section]:
                event_class = list(self.structured_data[section].keys())[0]
                ip = list(self.structured_data[section][event_class].keys())[0]
                return 'source' in self.structured_data[section][event_class][ip]


class ItemChangeLogModel(MODEL):
    """
    Class representing item changelog records within the SQL database mapped to
    ``changelogs_items`` table.
    """
    __tablename__ = 'changelogs_items'

    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id', onupdate = "CASCADE"))
    author    = sqlalchemy.orm.relationship('UserModel', back_populates = 'changelogs', enable_typechecks = False)
    model_id  = sqlalchemy.Column(sqlalchemy.Integer, nullable = False)
    model     = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    endpoint  = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    module    = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    operation = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    before    = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    after     = sqlalchemy.Column(sqlalchemy.String, nullable = False)
    diff      = sqlalchemy.Column(sqlalchemy.String, nullable = False)

    def __repr__(self):
        return "<ItemChangelog(author='%s',operation='%s',model='%s#%s')>" % (str(self.author), self.operation, self.model, self.model_id)

    def __str__(self):
        return 'ICL#{:d}:{:s}#{:d}:{:s}'.format(self.id, self.model, self.model_id, self.operation)

    def calculate_diff(self):
        """
        Calculate difference between internal ``before`` and ``after`` attributes
        and store it internally into ``diff`` attribute.
        """
        self.diff = jsondiff(self.before, self.after)


class DetectorModel(MODEL):  # pylint: disable=locally-disabled,too-few-public-methods
    """
    Class representing detectors objects within the SQL database mapped to
    ``detectors`` table.
    """
    __tablename__ = 'detectors'

    name = sqlalchemy.Column(sqlalchemy.String(100), unique = True, nullable = False, index = True)
    description = sqlalchemy.Column(sqlalchemy.String)
    source = sqlalchemy.Column(sqlalchemy.String(50), nullable = False)
    credibility = sqlalchemy.Column(sqlalchemy.Float, nullable = False)
    registered = sqlalchemy.Column(sqlalchemy.DateTime)
    hits = sqlalchemy.Column(sqlalchemy.Integer, default = 0, nullable = False)

    def __repr__(self):
        return "<Detector(name='%s')>" % (self.name)

    def to_dict(self):
        """
        *Interface implementation:* Implementation of :py:func:`mentat.datatype.sqldb.MODEL.to_dict` method.
        """
        return {
            'id': int(self.id),
            'createtime': str(self.createtime),
            'name': str(self.name),
            'source': str(self.source),
            'description': str(self.description),
            'credibility': float(self.credibility),
            'registered': str(self.registered),
            'hits': int(self.hits)
        }


def detectormodel_from_typeddict(structure, defaults = None):
    """
    Convenience method for creating :py:class:`mentat.datatype.sqldb.DetectorModel`
    object from :py:class:`mentat.datatype.internal.Detector` objects.
    """
    if not defaults:
        defaults = {}

    sqlobj = DetectorModel()
    sqlobj.name = structure.get('name')
    sqlobj.source = structure.get('source')
    sqlobj.credibility = structure.get('credibility', defaults.get('credibility', 1.0))
    sqlobj.description = structure.get('description', defaults.get('description', None))
    sqlobj.registered = structure.get('registered', defaults.get('registered', None))
    sqlobj.hits = structure.get('hits', 0)

    return sqlobj


#-------------------------------------------------------------------------------


def jsondiff(json_obj_a, json_obj_b):
    """
    Calculate the difference between two model objects given as JSON strings.
    """
    return "\n".join(
        difflib.unified_diff(json_obj_a.split("\n"), json_obj_b.split("\n"))
    )


def dictdiff(dict_obj_a, dict_obj_b):
    """
    Calculate the difference between two model objects given as dicts.
    """
    json_obj_a = json.dumps(dict_obj_a, indent = 4, sort_keys = True)
    json_obj_b = json.dumps(dict_obj_b, indent = 4, sort_keys = True)
    return jsondiff(json_obj_a, json_obj_b)


def diff(obj_a, obj_b):
    """
    Calculate the difference between two model objects given as dicts.
    """
    return jsondiff(obj_a.to_json(), obj_b.to_json())
