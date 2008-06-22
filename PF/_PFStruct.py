"""Mapping of C structs required by ioctl() calls to ctypes."""

from ctypes import *

from PFConstants import *


__all__ = ['pf_addr',
           'pf_addr_wrap',
           'pf_rule_addr',
           'pfioc_limit',
           'pfioc_tm',
           'pfioc_if',
           'pf_status',
           'pfioc_states',
           'pfsync_state_peer',
           'pfsync_state',
           'pfioc_state_kill',
           'pfioc_pooladdr',
           'pf_pool',
           'pf_rule',
           'pfioc_trans_e',
           'pfioc_trans',
           'pfioc_rule']


# Constants ####################################################################
IFNAMSIZ             = 16
PFRES_MAX            = 15
LCNT_MAX             = 7
FCNT_MAX             = 3
SCNT_MAX             = 3
PF_MD5_DIGEST_LENGTH = 16
PF_TABLE_NAME_SIZE   = 32
RTLABEL_LEN          = 32
MAXPATHLEN           = 1024
PF_SKIP_COUNT        = 8
PF_RULE_LABEL_SIZE   = 64
PF_QNAME_SIZE        = 64
PF_TAG_NAME_SIZE     = 64


# BufferStructure Class ########################################################
class BufferStructure(Structure):
    """A subclass of ctypes.Structure to simplify ioctl() system calls."""

    def __init__(self, **kw):
        """Call the parent constructor."""
        Structure.__init__(self, **kw)

    def asBuffer(self):
        """Return a buffer pointing to the Structure.

        This allows ioctl() to write directly to the structure, even if bigger
        than 1024 bytes.
        """
        return (c_char * sizeof(self)).from_address(addressof(self))


# Structures ###################################################################
class pf_addr(Structure):
    class _pfa(Union):
        _fields_ = [("v4",            c_uint32),
                    ("v6",            c_uint32 * 4),
                    ("addr8",         c_uint8 * 16),
                    ("addr16",        c_uint16 * 8),
                    ("addr32",        c_uint32 * 4)]

    _fields_ = [("pfa",               _pfa)]
    _anonymous_ = ("pfa",)

class pf_addr_wrap(Structure):

    class _v(Union):

        class _a(Structure):
            _fields_ = [("addr",      pf_addr),
                        ("mask",      pf_addr)]

        _fields_ = [("a",             _a),
                    ("ifname",        c_char * IFNAMSIZ),
                    ("tblname",       c_char * PF_TABLE_NAME_SIZE),
                    ("rtlabelname",   c_char * RTLABEL_LEN),
                    ("rtlabel",       c_uint32)]

    class _p(Union):
        _fields_ = [("dyn",           c_void_p),        # (struct pfi_dynaddr *)
                    ("tbl",           c_void_p),        # (struct pfr_ktable *)
                    ("dyncnt",        c_int),
                    ("tblcnt",        c_int)]

    _fields_ = [("v",                 _v),
                ("p",                 _p),
                ("type",              c_uint8),
                ("iflags",            c_uint8)]

class pf_rule_addr(Structure):
    _fields_ = [("addr",              pf_addr_wrap),
                ("port",              c_uint16 * 2),
                ("neg",               c_uint8),
                ("port_op",           c_uint8)]


class pfioc_limit(BufferStructure):
    _fields_ = [("index",             c_int),
                ("limit",             c_uint)]


class pfioc_tm(BufferStructure):
    _fields_ = [("timeout",           c_int),
                ("seconds",           c_int)]


class pfioc_if(BufferStructure):
    _fields_ = [("ifname",            c_char * IFNAMSIZ)]


class pf_status(BufferStructure):
    _fields_ = [("counters",          c_uint64 * PFRES_MAX),
                ("lcounters",         c_uint64 * LCNT_MAX),
                ("fcounters",         c_uint64 * FCNT_MAX),
                ("scounters",         c_uint64 * SCNT_MAX),
                ("pcounters",         c_uint64 * 3 * 2 * 2),
                ("bcounters",         c_uint64 * 2 * 2),
                ("stateid",           c_uint64),
                ("running",           c_uint32),
                ("states",            c_uint32),
                ("src_nodes",         c_uint32),
                ("since",             c_uint32),
                ("debug",             c_uint32),
                ("hostid",            c_uint32),
                ("ifname",            c_char * IFNAMSIZ),
                ("pf_chksum",         c_uint8 * PF_MD5_DIGEST_LENGTH)]


class pfioc_states(BufferStructure):
    class _ps_u(Union):
        _fields_ = [("ps_buf",        c_void_p),
                    ("ps_states",     c_void_p)]

    _fields_ = [("ps_len",            c_int),
                ("ps_u",              _ps_u)]
    _anonymous_ =  ("ps_u",)

class pfsync_state_host(Structure):
    _fields_ = [("addr",              pf_addr),
                ("port",              c_uint16),
                ("pad",               c_uint16 * 3)]

class pfsync_state_scrub(Structure):
    _fields_ = [("pfss_flags",        c_uint16),
                ("pfss_ttl",          c_uint8),
                ("scrub_flag",        c_uint8),
                ("pfss_ts_mod",       c_uint32)]

class pfsync_state_peer(Structure):
    _fields_ = [("scrub",             pfsync_state_scrub),
                ("seqlo",             c_uint32),
                ("seqhi",             c_uint32),
                ("seqdiff",           c_uint32),
                ("max_win",           c_uint16),
                ("mss",               c_uint16),
                ("state",             c_uint8),
                ("wscale",            c_uint8),
                ("pad",               c_uint8 * 6)]

class pfsync_state(Structure):
    _fields_ = [("id",                c_uint32 * 2),
                ("ifname",            c_char * IFNAMSIZ),
                ("lan",               pfsync_state_host),
                ("gwy",               pfsync_state_host),
                ("ext",               pfsync_state_host),
                ("src",               pfsync_state_peer),
                ("dst",               pfsync_state_peer),
                ("rt_addr",           pf_addr),
                ("rule",              c_uint32),
                ("anchor",            c_uint32),
                ("nat_rule",          c_uint32),
                ("creation",          c_uint32),
                ("expire",            c_uint32),
                ("packets",           c_uint32 * 2 * 2),
                ("bytes",             c_uint32 * 2 * 2),
                ("creatorid",         c_uint32),
                ("af",                c_uint8),
                ("proto",             c_uint8),
                ("direction",         c_uint8),
                ("log",               c_uint8),
                ("allow_opts",        c_uint8),
                ("timeout",           c_uint8),
                ("sync_flags",        c_uint8),
                ("updates",           c_uint8)]

class pfioc_state_kill(BufferStructure):
    _fields_ = [("psk_af",            c_uint8),
                ("psk_proto",         c_int),
                ("psk_src",           pf_rule_addr),
                ("psk_dst",           pf_rule_addr),
                ("psk_ifname",        c_char * IFNAMSIZ)]


class pf_poolhashkey(Structure):

    class _pfk(Union):
        _fields_ = [("key8",          c_uint8 * 16),
                    ("key16",         c_uint16 * 8),
                    ("key32",         c_uint32 * 4)]

    _fields_ = [("pfk",               _pfk)]
    _anonymous_ = ("pfk",)

class pf_pooladdr(Structure):
    _fields_ = [("addr",              pf_addr_wrap),
                ("entries",           c_void_p * 2),  # TAILQ_ENTRY(pf_pooladdr)
                ("ifname",            c_char * IFNAMSIZ),
                ("kif",               c_void_p)]      # (struct pfi_kif *)

class pfioc_pooladdr(BufferStructure):
    _fields_ = [("action",            c_uint32),
                ("ticket",            c_uint32),
                ("nr",                c_uint32),
                ("r_num",             c_uint32),
                ("r_action",          c_uint8),
                ("r_last",            c_uint8),
                ("af",                c_uint8),
                ("anchor",            c_char * MAXPATHLEN),
                ("addr",              pf_pooladdr)]

class pf_palist(Structure):
    _fields_ = [("tqh_first",         POINTER(pf_pooladdr)),
                ("tqh_last",          POINTER(pf_pooladdr))]

class pf_pool(Structure):
    _fields_ = [("list",              pf_palist),
                ("cur",               POINTER(pf_pooladdr)),
                ("key",               pf_poolhashkey),
                ("counter",           pf_addr),
                ("tblidx",            c_int),
                ("proxy_port",        c_uint16 * 2),
                ("port_op",           c_uint8),
                ("opts",              c_uint8)]

class pf_rule_uid(Structure):
    _fields_ = [("uid",               c_uint32 * 2),
                ("op",                c_uint8)]

class pf_rule_gid(Structure):
    _fields_ = [("gid",               c_uint32 * 2),
                ("op",                c_uint8)]

class pf_rule_ptr(Union):
    _fields_ = [("ptr",               c_void_p),        # (pf_rule *)
                ("nr",                c_uint32)]

class pf_rule(Structure):

    class _conn_rate(Structure):
        _fields_ = [("limit",         c_uint32),
                    ("seconds",       c_uint32)]

    _fields_ = [("src",               pf_rule_addr),
                ("dst",               pf_rule_addr),
                ("skip",              pf_rule_ptr * PF_SKIP_COUNT),
                ("label",             c_char * PF_RULE_LABEL_SIZE),
                ("ifname",            c_char * IFNAMSIZ),
                ("qname",             c_char * PF_QNAME_SIZE),
                ("pqname",            c_char * PF_QNAME_SIZE),
                ("tagname",           c_char * PF_TAG_NAME_SIZE),
                ("match_tagname",     c_char * PF_TAG_NAME_SIZE),
                ("overload_tblname",  c_char * PF_TABLE_NAME_SIZE),
                ("entries",           c_void_p * 2),    # TAILQ_ENTRY(pf_rule)
                ("rpool",             pf_pool),
                ("evaluations",       c_uint64),
                ("packets",           c_uint64 * 2),
                ("bytes",             c_uint64 * 2),
                ("kif",               c_void_p),        # (struct pki_kif *)
                ("anchor",            c_void_p),        # (struct pf_anchor *)
                ("overload_tbl",      c_void_p),        # (struct pfr_table *)
                ("os_fingerprint",    c_uint32),
                ("rtableid",          c_int),
                ("timeout",           c_uint32 * PFTM_MAX),
                ("states",            c_uint32),
                ("max_states",        c_uint32),
                ("src_nodes",         c_uint32),
                ("max_src_nodes",     c_uint32),
                ("max_src_states",    c_uint32),
                ("max_src_conn",      c_uint32),
                ("max_src_conn_rate", _conn_rate),
                ("qid",               c_uint32),
                ("pqid",              c_uint32),
                ("rt_listid",         c_uint32),
                ("nr",                c_uint32),
                ("prob",              c_uint32),
                ("cuid",              c_uint32),
                ("cpid",              c_int32),
                ("return_icmp",       c_uint16),
                ("return_icmp6",      c_uint16),
                ("max_mss",           c_uint16),
                ("tag",               c_uint16),
                ("match_tag",         c_uint16),
                ("uid",               pf_rule_uid),
                ("gid",               pf_rule_gid),
                ("rule_flag",         c_uint32),
                ("action",            c_uint8),
                ("direction",         c_uint8),
                ("log",               c_uint8),
                ("logif",             c_uint8),
                ("quick",             c_uint8),
                ("ifnot",             c_uint8),
                ("match_tag_not",     c_uint8),
                ("natpass",           c_uint8),
                ("keep_state",        c_uint8),
                ("af",                c_uint8),
                ("proto",             c_uint8),
                ("type",              c_uint8),
                ("code",              c_uint8),
                ("flags",             c_uint8),
                ("flagset",           c_uint8),
                ("min_ttl",           c_uint8),
                ("allow_opts",        c_uint8),
                ("rt",                c_uint8),
                ("return_ttl",        c_uint8),
                ("tos",               c_uint8),
                ("anchor_relative",   c_uint8),
                ("anchor_wildcard",   c_uint8),
                ("flush",             c_uint8)]

class pfioc_rule(BufferStructure):
    _fields_ = [("action",            c_uint32),
                ("ticket",            c_uint32),
                ("pool_ticket",       c_uint32),
                ("nr",                c_uint32),
                ("anchor",            c_char * MAXPATHLEN),
                ("anchor_call",       c_char * MAXPATHLEN),
                ("rule",              pf_rule)]

class pfioc_trans_e(Structure):
    _fields_ = [("rs_num",        c_int),
                ("anchor",        c_char * MAXPATHLEN),
                ("ticket",        c_uint32)]

class pfioc_trans(BufferStructure):
    _fields_ = [("size",              c_int),
                ("esize",             c_int),
                ("array",             c_void_p)]

