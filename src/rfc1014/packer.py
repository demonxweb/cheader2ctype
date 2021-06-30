from cgfsm.nfsv4.nfsstruct import const
from cgfsm.nfsv4.nfsstruct.pack import Pack,Packer,UnPacker
class NFSPacker(Packer):
    int32_t = Packer.int
    uint32_t = Packer.uint
    int64_t = Packer.hyper
    uint64_t = Packer.uhyper
    attrlist4 = Packer.opaque
    def bitmap4(self,x):
        return self._array(x,self.uint32_t,limit=None)

    changeid4 = uint64_t
    clientid4 = uint64_t
    count4 = uint32_t
    length4 = uint64_t
    mode4 = uint32_t
    nfs_cookie4 = uint64_t
    def nfs_fh4(self,x):
        self.opaque(x,limit=const.NFS4_FHSIZE)

    nfs_ftype4 = Packer.enum
    nfsstat4 = Packer.enum
    time_how4 = Packer.enum
    opentype4 = Packer.enum
    open_claim_type4 = Packer.enum
    open_delegation_type4 = Packer.enum
    limit_by4 = Packer.enum
    createmode4 = Packer.enum
    stable_how4 = Packer.enum
    nfs_lease4 = uint32_t
    offset4 = uint64_t
    qop4 = uint32_t
    sec_oid4 = Packer.opaque
    seqid4 = uint32_t
    utf8string = Packer.opaque
    utf8str_cis = utf8string
    utf8str_cs = utf8string
    utf8str_mixed = utf8string
    component4 = utf8str_cs
    linktext4 = Packer.opaque
    ascii_REQUIRED4 = utf8string
    def pathname4(self,x):
        return self._array(x,self.component4,limit=None)

    nfs_lockid4 = uint64_t
    def verifier4(self,x):
        self.opaque(x,fixed=const.NFS4_VERIFIER_SIZE)

    def specdata4(self,pk):
        self.uint32_t(pk.specdata1)
        self.uint32_t(pk.specdata2)

    def fsid4(self,pk):
        self.uint64_t(pk.major)
        self.uint64_t(pk.minor)

    def fs_location4(self,pk):
        self.opaque(pk.server,limit=None)
        self.pathname4(pk.rootpath)

    def fs_locations4(self,pk):
        self.pathname4(pk.fs_root)
        self._array(pk.locations,self.fs_location4,limit=None)

    def fattr4(self,pk):
        self.bitmap4(pk.attrmask)
        self.attrlist4(pk.attr_vals)

    def change_info4(self,pk):
        self.bool(pk.atomic)
        self.changeid4(pk.before)
        self.changeid4(pk.after)

    def clientaddr4(self,pk):
        self.opaque(pk.r_netid,limit=None)
        self.opaque(pk.r_addr,limit=None)

    def cb_client4(self,pk):
        self.uint(pk.cb_program)
        self.clientaddr4(pk.cb_location)

    def nfs_client_id4(self,pk):
        self.verifier4(pk.verifier)
        self.opaque(pk.id,limit=const.NFS4_OPAQUE_LIMIT)

    def open_owner4(self,pk):
        self.clientid4(pk.clientid)
        self.opaque(pk.owner,limit=const.NFS4_OPAQUE_LIMIT)

    def lock_owner4(self,pk):
        self.clientid4(pk.clientid)
        self.opaque(pk.owner,limit=const.NFS4_OPAQUE_LIMIT)

    def open_to_lock_owner4(self,pk):
        self.seqid4(pk.open_seqid)
        self.stateid4(pk.open_stateid)
        self.seqid4(pk.lock_seqid)
        self.lock_owner4(pk.lock_owner)

    def stateid4(self,pk):
        self.uint32_t(pk.seqid)
        self.opaque(pk.other,fixed=const.NFS4_OTHER_SIZE)

    def nfsace4(self,pk):
        self.acetype4(pk.type)
        self.aceflag4(pk.flag)
        self.acemask4(pk.access_mask)
        self.utf8str_mixed(pk.who)

    def nfstime4(self,pk):
        self.int64_t(pk.seconds)
        self.uint32_t(pk.nseconds)

    def COMPOUND4args(self,pk):
        self.utf8str_cs(pk.tag)
        self.uint32_t(pk.minorversion)
        self._array(pk.argarray,self.nfs_argop4,limit=None)

    def COMPOUND4res(self,pk):
        self.nfsstat4(pk.status)
        self.utf8str_cs(pk.tag)
        self._array(pk.resarray,self.nfs_resop4,limit=None)

    def ACCESS4args(self,pk):
        self.uint32_t(pk.access)

    def ACCESS4resok(self,pk):
        self.uint32_t(pk.supported)
        self.uint32_t(pk.access)

    def CLOSE4args(self,pk):
        self.seqid4(pk.seqid)
        self.stateid4(pk.open_stateid)

    def COMMIT4args(self,pk):
        self.offset4(pk.offset)
        self.count4(pk.count)

    def COMMIT4resok(self,pk):
        self.verifier4(pk.writeverf)

    def CREATE4args(self,pk):
        self.createtype4(pk.objtype)
        self.component4(pk.objname)
        self.fattr4(pk.createattrs)

    def CREATE4resok(self,pk):
        self.change_info4(pk.cinfo)
        self.bitmap4(pk.attrset)

    def DELEGPURGE4args(self,pk):
        self.clientid4(pk.clientid)

    def DELEGPURGE4res(self,pk):
        self.nfsstat4(pk.status)

    def DELEGRETURN4args(self,pk):
        self.stateid4(pk.deleg_stateid)

    def DELEGRETURN4res(self,pk):
        self.nfsstat4(pk.status)

    def GETATTR4args(self,pk):
        self.bitmap4(pk.attr_request)

    def GETATTR4resok(self,pk):
        self.fattr4(pk.obj_attributes)

    def GETFH4resok(self,pk):
        self.nfs_fh4(pk.object)

    def LINK4args(self,pk):
        self.component4(pk.newname)

    def LINK4resok(self,pk):
        self.change_info4(pk.cinfo)

    def open_to_lock_owner4(self,pk):
        self.seqid4(pk.open_seqid)
        self.stateid4(pk.open_stateid)
        self.seqid4(pk.lock_seqid)
        self.lock_owner4(pk.lock_owner)

    def exist_lock_owner4(self,pk):
        self.stateid4(pk.lock_stateid)
        self.seqid4(pk.lock_seqid)

    def LOCK4args(self,pk):
        self.nfs_lock_type4(pk.locktype)
        self.bool(pk.reclaim)
        self.offset4(pk.offset)
        self.length4(pk.length)
        self.locker4(pk.locker)

    def LOCK4denied(self,pk):
        self.offset4(pk.offset)
        self.length4(pk.length)
        self.nfs_lock_type4(pk.locktype)
        self.lock_owner4(pk.owner)

    def LOCK4resok(self,pk):
        self.stateid4(pk.lock_stateid)

    def LOCKT4args(self,pk):
        self.nfs_lock_type4(pk.locktype)
        self.offset4(pk.offset)
        self.length4(pk.length)
        self.lock_owner4(pk.owner)

    def LOCKU4args(self,pk):
        self.nfs_lock_type4(pk.locktype)
        self.seqid4(pk.seqid)
        self.stateid4(pk.lock_stateid)
        self.offset4(pk.offset)
        self.length4(pk.length)

    def LOOKUP4args(self,pk):
        self.component4(pk.objname)

    def LOOKUP4res(self,pk):
        self.nfsstat4(pk.status)

    def LOOKUPP4res(self,pk):
        self.nfsstat4(pk.status)

    def NVERIFY4args(self,pk):
        self.fattr4(pk.obj_attributes)

    def NVERIFY4res(self,pk):
        self.nfsstat4(pk.status)

    def nfs_modified_limit4(self,pk):
        self.uint32_t(pk.num_blocks)
        self.uint32_t(pk.bytes_per_block)

    def open_claim_delegate_cur4(self,pk):
        self.stateid4(pk.delegate_stateid)
        self.component4(pk.file)

    def OPEN4args(self,pk):
        self.seqid4(pk.seqid)
        self.uint32_t(pk.share_access)
        self.uint32_t(pk.share_deny)
        self.open_owner4(pk.owner)
        self.openflag4(pk.openhow)
        self.open_claim4(pk.claim)

    def open_read_delegation4(self,pk):
        self.stateid4(pk.stateid)
        self.bool(pk.recall)
        self.nfsace4(pk.permissions)

    def open_write_delegation4(self,pk):
        self.stateid4(pk.stateid)
        self.bool(pk.recall)
        self.nfs_space_limit4(pk.space_limit)
        self.nfsace4(pk.permissions)

    def OPEN4resok(self,pk):
        self.stateid4(pk.stateid)
        self.change_info4(pk.cinfo)
        self.uint32_t(pk.rflags)
        self.bitmap4(pk.attrset)
        self.open_delegation4(pk.delegation)

    def OPENATTR4args(self,pk):
        self.bool(pk.createdir)

    def OPENATTR4res(self,pk):
        self.nfsstat4(pk.status)

    def OPEN_CONFIRM4args(self,pk):
        self.stateid4(pk.open_stateid)
        self.seqid4(pk.seqid)

    def OPEN_CONFIRM4resok(self,pk):
        self.stateid4(pk.open_stateid)

    def OPEN_DOWNGRADE4args(self,pk):
        self.stateid4(pk.open_stateid)
        self.seqid4(pk.seqid)
        self.uint32_t(pk.share_access)
        self.uint32_t(pk.share_deny)

    def OPEN_DOWNGRADE4resok(self,pk):
        self.stateid4(pk.open_stateid)

    def PUTFH4args(self,pk):
        self.nfs_fh4(pk.object)

    def PUTFH4res(self,pk):
        self.nfsstat4(pk.status)

    def PUTPUBFH4res(self,pk):
        self.nfsstat4(pk.status)

    def PUTROOTFH4res(self,pk):
        self.nfsstat4(pk.status)

    def READ4args(self,pk):
        self.stateid4(pk.stateid)
        self.offset4(pk.offset)
        self.count4(pk.count)

    def READ4resok(self,pk):
        self.bool(pk.eof)
        self.opaque(pk.data,limit=None)

    def READDIR4args(self,pk):
        self.nfs_cookie4(pk.cookie)
        self.verifier4(pk.cookieverf)
        self.count4(pk.dircount)
        self.count4(pk.maxcount)
        self.bitmap4(pk.attr_request)

    def entry4(self,pk):
        self.nfs_cookie4(pk.cookie)
        self.component4(pk.name)
        self.fattr4(pk.attrs)
        # recursive entry4 *nextentry 
        self._array(pk.nextentry,self.entry4)

    def dirlist4(self,pk):
        # recursive entry4 *entries 
        self._array(pk.entries,self.entry4)
        self.bool(pk.eof)

    def READDIR4resok(self,pk):
        self.verifier4(pk.cookieverf)
        self.dirlist4(pk.reply)

    def READLINK4resok(self,pk):
        self.linktext4(pk.link)

    def REMOVE4args(self,pk):
        self.component4(pk.target)

    def REMOVE4resok(self,pk):
        self.change_info4(pk.cinfo)

    def RENAME4args(self,pk):
        self.component4(pk.oldname)
        self.component4(pk.newname)

    def RENAME4resok(self,pk):
        self.change_info4(pk.source_cinfo)
        self.change_info4(pk.target_cinfo)

    def RENEW4args(self,pk):
        self.clientid4(pk.clientid)

    def RENEW4res(self,pk):
        self.nfsstat4(pk.status)

    def RESTOREFH4res(self,pk):
        self.nfsstat4(pk.status)

    def SAVEFH4res(self,pk):
        self.nfsstat4(pk.status)

    def SECINFO4args(self,pk):
        self.component4(pk.name)

    def rpcsec_gss_info(self,pk):
        self.sec_oid4(pk.oid)
        self.qop4(pk.qop)
        self.rpc_gss_svc_t(pk.service)

    def SETATTR4args(self,pk):
        self.stateid4(pk.stateid)
        self.fattr4(pk.obj_attributes)

    def SETATTR4res(self,pk):
        self.nfsstat4(pk.status)
        self.bitmap4(pk.attrsset)

    def SETCLIENTID4args(self,pk):
        self.nfs_client_id4(pk.client)
        self.cb_client4(pk.callback)
        self.uint32_t(pk.callback_ident)

    def SETCLIENTID4resok(self,pk):
        self.clientid4(pk.clientid)
        self.verifier4(pk.setclientid_confirm)

    def SETCLIENTID_CONFIRM4args(self,pk):
        self.clientid4(pk.clientid)
        self.verifier4(pk.setclientid_confirm)

    def SETCLIENTID_CONFIRM4res(self,pk):
        self.nfsstat4(pk.status)

    def VERIFY4args(self,pk):
        self.fattr4(pk.obj_attributes)

    def VERIFY4res(self,pk):
        self.nfsstat4(pk.status)

    def WRITE4args(self,pk):
        self.stateid4(pk.stateid)
        self.offset4(pk.offset)
        self.stable_how4(pk.stable)
        self.opaque(pk.data,limit=None)

    def WRITE4resok(self,pk):
        self.count4(pk.count)
        self.stable_how4(pk.committed)
        self.verifier4(pk.writeverf)

    def RELEASE_LOCKOWNER4args(self,pk):
        self.lock_owner4(pk.lock_owner)

    def RELEASE_LOCKOWNER4res(self,pk):
        self.nfsstat4(pk.status)

    def ILLEGAL4res(self,pk):
        self.nfsstat4(pk.status)

    def CB_COMPOUND4args(self,pk):
        self.utf8str_cs(pk.tag)
        self.uint32_t(pk.minorversion)
        self.uint32_t(pk.callback_ident)
        self._array(pk.argarray,self.nfs_cb_argop4,limit=None)

    def CB_COMPOUND4res(self,pk):
        self.nfsstat4(pk.status)
        self.utf8str_cs(pk.tag)
        self._array(pk.resarray,self.nfs_cb_resop4,limit=None)

    def CB_GETATTR4args(self,pk):
        self.nfs_fh4(pk.fh)
        self.bitmap4(pk.attr_request)

    def CB_GETATTR4resok(self,pk):
        self.fattr4(pk.obj_attributes)

    def CB_RECALL4args(self,pk):
        self.stateid4(pk.stateid)
        self.bool(pk.truncate)
        self.nfs_fh4(pk.fh)

    def CB_RECALL4res(self,pk):
        self.nfsstat4(pk.status)

    def CB_ILLEGAL4res(self,pk):
        self.nfsstat4(pk.status)

    def settime4(self,pk):
        self.time_how4(pk.set_it)
        if pk.set_it in [const.SET_TO_CLIENT_TIME4]:
            self.nfstime4(pk.time)
    def ACCESS4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.ACCESS4resok(pk.resok4)
    def CLOSE4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.stateid4(pk.open_stateid)
    def COMMIT4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.COMMIT4resok(pk.resok4)
    def createtype4(self,pk):
        self.nfs_ftype4(pk.type)
        if pk.type in [const.NF4LNK]:
            self.linktext4(pk.linkdata)
        elif pk.type in [const.NF4BLK,const.NF4CHR]:
            self.specdata4(pk.devdata)
    def CREATE4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.CREATE4resok(pk.resok4)
    def GETATTR4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.GETATTR4resok(pk.resok4)
    def GETFH4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.GETFH4resok(pk.resok4)
    def LINK4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.LINK4resok(pk.resok4)
    def locker4(self,pk):
        self.bool(pk.new_lock_owner)
        if pk.new_lock_owner in [const.TRUE]:
            self.open_to_lock_owner4(pk.open_owner)
        elif pk.new_lock_owner in [const.FALSE]:
            self.exist_lock_owner4(pk.lock_owner)
    def LOCK4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.LOCK4resok(pk.resok4)
        elif pk.status in [const.NFS4ERR_DENIED]:
            self.LOCK4denied(pk.denied)
    def LOCKT4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4ERR_DENIED]:
            self.LOCK4denied(pk.denied)
    def LOCKU4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.stateid4(pk.lock_stateid)
    def createhow4(self,pk):
        self.createmode4(pk.mode)
        if pk.mode in [const.UNCHECKED4,const.GUARDED4]:
            self.fattr4(pk.createattrs)
        elif pk.mode in [const.EXCLUSIVE4]:
            self.verifier4(pk.createverf)
    def openflag4(self,pk):
        self.opentype4(pk.opentype)
        if pk.opentype in [const.OPEN4_CREATE]:
            self.createhow4(pk.how)
    def nfs_space_limit4(self,pk):
        self.limit_by4(pk.limitby)
        if pk.limitby in [const.NFS_LIMIT_SIZE]:
            self.uint64_t(pk.filesize)
        elif pk.limitby in [const.NFS_LIMIT_BLOCKS]:
            self.nfs_modified_limit4(pk.mod_blocks)
    def open_claim4(self,pk):
        self.open_claim_type4(pk.claim)
        if pk.claim in [const.CLAIM_NULL]:
            self.component4(pk.file)
        elif pk.claim in [const.CLAIM_PREVIOUS]:
            self.open_delegation_type4(pk.delegate_type)
        elif pk.claim in [const.CLAIM_DELEGATE_CUR]:
            self.open_claim_delegate_cur4(pk.delegate_cur_info)
        elif pk.claim in [const.CLAIM_DELEGATE_PREV]:
            self.component4(pk.file_delegate_prev)
    def open_delegation4(self,pk):
        self.open_delegation_type4(pk.delegation_type)
        if pk.delegation_type in [const.OPEN_DELEGATE_READ]:
            self.open_read_delegation4(pk.read)
        elif pk.delegation_type in [const.OPEN_DELEGATE_WRITE]:
            self.open_write_delegation4(pk.write)
    def OPEN4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.OPEN4resok(pk.resok4)
    def OPEN_CONFIRM4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.OPEN_CONFIRM4resok(pk.resok4)
    def OPEN_DOWNGRADE4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.OPEN_DOWNGRADE4resok(pk.resok4)
    def READ4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.READ4resok(pk.resok4)
    def READDIR4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.READDIR4resok(pk.resok4)
    def READLINK4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.READLINK4resok(pk.resok4)
    def REMOVE4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.REMOVE4resok(pk.resok4)
    def RENAME4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.RENAME4resok(pk.resok4)
    def secinfo4(self,pk):
        self.uint32_t(pk.flavor)
        if pk.flavor in [const.RPCSEC_GSS]:
            self.rpcsec_gss_info(pk.flavor_info)
    def SECINFO4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.SECINFO4resok(pk.resok4)
    def SETCLIENTID4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.SETCLIENTID4resok(pk.resok4)
        elif pk.status in [const.NFS4ERR_CLID_INUSE]:
            self.clientaddr4(pk.client_using)
    def WRITE4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.WRITE4resok(pk.resok4)
    def nfs_cb_argop4(self,pk):
        self.unsigned(pk.argop)
        if pk.argop in [const.OP_CB_GETATTR]:
            self.CB_GETATTR4args(pk.opcbgetattr)
        elif pk.argop in [const.OP_CB_RECALL]:
            self.CB_RECALL4args(pk.opcbrecall)
    def nfs_cb_resop4(self,pk):
        self.unsigned(pk.resop)
        if pk.resop in [const.OP_CB_GETATTR]:
            self.CB_GETATTR4res(pk.opcbgetattr)
        elif pk.resop in [const.OP_CB_RECALL]:
            self.CB_RECALL4res(pk.opcbrecall)
        elif pk.resop in [const.OP_CB_ILLEGAL]:
            self.CB_ILLEGAL4res(pk.opcbillegal)
    def CB_GETATTR4res(self,pk):
        self.nfsstat4(pk.status)
        if pk.status in [const.NFS4_OK]:
            self.CB_GETATTR4resok(pk.resok4)
class NFSUnPacker(UnPacker):
    int32_t = UnPacker.int
    uint32_t = UnPacker.uint
    int64_t = UnPacker.hyper
    uint64_t = UnPacker.uhyper
    attrlist4 = UnPacker.opaque
    def bitmap4(self):
        return self._array(self.uint32_t,limit=None)

    changeid4 = uint64_t
    clientid4 = uint64_t
    count4 = uint32_t
    length4 = uint64_t
    mode4 = uint32_t
    nfs_cookie4 = uint64_t
    def nfs_fh4(self):
        return self.opaque(limit=const.NFS4_FHSIZE)

    nfs_ftype4 = UnPacker.enum
    nfsstat4 = UnPacker.enum
    time_how4 = UnPacker.enum
    opentype4 = UnPacker.enum
    open_claim_type4 = UnPacker.enum
    open_delegation_type4 = UnPacker.enum
    limit_by4 = UnPacker.enum
    createmode4 = UnPacker.enum
    stable_how4 = UnPacker.enum
    nfs_lease4 = uint32_t
    offset4 = uint64_t
    qop4 = uint32_t
    sec_oid4 = UnPacker.opaque
    seqid4 = uint32_t
    utf8string = UnPacker.opaque
    utf8str_cis = utf8string
    utf8str_cs = utf8string
    utf8str_mixed = utf8string
    component4 = utf8str_cs
    linktext4 = UnPacker.opaque
    ascii_REQUIRED4 = utf8string
    def pathname4(self):
        return self._array(self.component4,limit=None)

    nfs_lockid4 = uint64_t
    def verifier4(self):
        return self.opaque(fixed=const.NFS4_VERIFIER_SIZE)

    def specdata4(self):
        pk = Pack('specdata4')
        pk.specdata1 = self.uint32_t()
        pk.specdata2 = self.uint32_t()
        return pk

    def fsid4(self):
        pk = Pack('fsid4')
        pk.major = self.uint64_t()
        pk.minor = self.uint64_t()
        return pk

    def fs_location4(self):
        pk = Pack('fs_location4')
        pk.server = self.opaque(limit=None)
        pk.rootpath = self.pathname4()
        return pk

    def fs_locations4(self):
        pk = Pack('fs_locations4')
        pk.fs_root = self.pathname4()
        pk.locations = self._array(self.fs_location4,limit=None)
        return pk

    def fattr4(self):
        pk = Pack('fattr4')
        pk.attrmask = self.bitmap4()
        pk.attr_vals = self.attrlist4()
        return pk

    def change_info4(self):
        pk = Pack('change_info4')
        pk.atomic = self.bool()
        pk.before = self.changeid4()
        pk.after = self.changeid4()
        return pk

    def clientaddr4(self):
        pk = Pack('clientaddr4')
        pk.r_netid = self.opaque(limit=None)
        pk.r_addr = self.opaque(limit=None)
        return pk

    def cb_client4(self):
        pk = Pack('cb_client4')
        pk.cb_program = self.uint()
        pk.cb_location = self.clientaddr4()
        return pk

    def nfs_client_id4(self):
        pk = Pack('nfs_client_id4')
        pk.verifier = self.verifier4()
        pk.id = self.opaque(limit=const.NFS4_OPAQUE_LIMIT)
        return pk

    def open_owner4(self):
        pk = Pack('open_owner4')
        pk.clientid = self.clientid4()
        pk.owner = self.opaque(limit=const.NFS4_OPAQUE_LIMIT)
        return pk

    def lock_owner4(self):
        pk = Pack('lock_owner4')
        pk.clientid = self.clientid4()
        pk.owner = self.opaque(limit=const.NFS4_OPAQUE_LIMIT)
        return pk

    def open_to_lock_owner4(self):
        pk = Pack('open_to_lock_owner4')
        pk.open_seqid = self.seqid4()
        pk.open_stateid = self.stateid4()
        pk.lock_seqid = self.seqid4()
        pk.lock_owner = self.lock_owner4()
        return pk

    def stateid4(self):
        pk = Pack('stateid4')
        pk.seqid = self.uint32_t()
        pk.other = self.opaque(fixed=const.NFS4_OTHER_SIZE)
        return pk

    def nfsace4(self):
        pk = Pack('nfsace4')
        pk.type = self.acetype4()
        pk.flag = self.aceflag4()
        pk.access_mask = self.acemask4()
        pk.who = self.utf8str_mixed()
        return pk

    def nfstime4(self):
        pk = Pack('nfstime4')
        pk.seconds = self.int64_t()
        pk.nseconds = self.uint32_t()
        return pk

    def COMPOUND4args(self):
        pk = Pack('COMPOUND4args')
        pk.tag = self.utf8str_cs()
        pk.minorversion = self.uint32_t()
        pk.argarray = self._array(self.nfs_argop4,limit=None)
        return pk

    def COMPOUND4res(self):
        pk = Pack('COMPOUND4res')
        pk.status = self.nfsstat4()
        pk.tag = self.utf8str_cs()
        pk.resarray = self._array(self.nfs_resop4,limit=None)
        return pk

    def ACCESS4args(self):
        pk = Pack('ACCESS4args')
        pk.access = self.uint32_t()
        return pk

    def ACCESS4resok(self):
        pk = Pack('ACCESS4resok')
        pk.supported = self.uint32_t()
        pk.access = self.uint32_t()
        return pk

    def CLOSE4args(self):
        pk = Pack('CLOSE4args')
        pk.seqid = self.seqid4()
        pk.open_stateid = self.stateid4()
        return pk

    def COMMIT4args(self):
        pk = Pack('COMMIT4args')
        pk.offset = self.offset4()
        pk.count = self.count4()
        return pk

    def COMMIT4resok(self):
        pk = Pack('COMMIT4resok')
        pk.writeverf = self.verifier4()
        return pk

    def CREATE4args(self):
        pk = Pack('CREATE4args')
        pk.objtype = self.createtype4()
        pk.objname = self.component4()
        pk.createattrs = self.fattr4()
        return pk

    def CREATE4resok(self):
        pk = Pack('CREATE4resok')
        pk.cinfo = self.change_info4()
        pk.attrset = self.bitmap4()
        return pk

    def DELEGPURGE4args(self):
        pk = Pack('DELEGPURGE4args')
        pk.clientid = self.clientid4()
        return pk

    def DELEGPURGE4res(self):
        pk = Pack('DELEGPURGE4res')
        pk.status = self.nfsstat4()
        return pk

    def DELEGRETURN4args(self):
        pk = Pack('DELEGRETURN4args')
        pk.deleg_stateid = self.stateid4()
        return pk

    def DELEGRETURN4res(self):
        pk = Pack('DELEGRETURN4res')
        pk.status = self.nfsstat4()
        return pk

    def GETATTR4args(self):
        pk = Pack('GETATTR4args')
        pk.attr_request = self.bitmap4()
        return pk

    def GETATTR4resok(self):
        pk = Pack('GETATTR4resok')
        pk.obj_attributes = self.fattr4()
        return pk

    def GETFH4resok(self):
        pk = Pack('GETFH4resok')
        pk.object = self.nfs_fh4()
        return pk

    def LINK4args(self):
        pk = Pack('LINK4args')
        pk.newname = self.component4()
        return pk

    def LINK4resok(self):
        pk = Pack('LINK4resok')
        pk.cinfo = self.change_info4()
        return pk

    def open_to_lock_owner4(self):
        pk = Pack('open_to_lock_owner4')
        pk.open_seqid = self.seqid4()
        pk.open_stateid = self.stateid4()
        pk.lock_seqid = self.seqid4()
        pk.lock_owner = self.lock_owner4()
        return pk

    def exist_lock_owner4(self):
        pk = Pack('exist_lock_owner4')
        pk.lock_stateid = self.stateid4()
        pk.lock_seqid = self.seqid4()
        return pk

    def LOCK4args(self):
        pk = Pack('LOCK4args')
        pk.locktype = self.nfs_lock_type4()
        pk.reclaim = self.bool()
        pk.offset = self.offset4()
        pk.length = self.length4()
        pk.locker = self.locker4()
        return pk

    def LOCK4denied(self):
        pk = Pack('LOCK4denied')
        pk.offset = self.offset4()
        pk.length = self.length4()
        pk.locktype = self.nfs_lock_type4()
        pk.owner = self.lock_owner4()
        return pk

    def LOCK4resok(self):
        pk = Pack('LOCK4resok')
        pk.lock_stateid = self.stateid4()
        return pk

    def LOCKT4args(self):
        pk = Pack('LOCKT4args')
        pk.locktype = self.nfs_lock_type4()
        pk.offset = self.offset4()
        pk.length = self.length4()
        pk.owner = self.lock_owner4()
        return pk

    def LOCKU4args(self):
        pk = Pack('LOCKU4args')
        pk.locktype = self.nfs_lock_type4()
        pk.seqid = self.seqid4()
        pk.lock_stateid = self.stateid4()
        pk.offset = self.offset4()
        pk.length = self.length4()
        return pk

    def LOOKUP4args(self):
        pk = Pack('LOOKUP4args')
        pk.objname = self.component4()
        return pk

    def LOOKUP4res(self):
        pk = Pack('LOOKUP4res')
        pk.status = self.nfsstat4()
        return pk

    def LOOKUPP4res(self):
        pk = Pack('LOOKUPP4res')
        pk.status = self.nfsstat4()
        return pk

    def NVERIFY4args(self):
        pk = Pack('NVERIFY4args')
        pk.obj_attributes = self.fattr4()
        return pk

    def NVERIFY4res(self):
        pk = Pack('NVERIFY4res')
        pk.status = self.nfsstat4()
        return pk

    def nfs_modified_limit4(self):
        pk = Pack('nfs_modified_limit4')
        pk.num_blocks = self.uint32_t()
        pk.bytes_per_block = self.uint32_t()
        return pk

    def open_claim_delegate_cur4(self):
        pk = Pack('open_claim_delegate_cur4')
        pk.delegate_stateid = self.stateid4()
        pk.file = self.component4()
        return pk

    def OPEN4args(self):
        pk = Pack('OPEN4args')
        pk.seqid = self.seqid4()
        pk.share_access = self.uint32_t()
        pk.share_deny = self.uint32_t()
        pk.owner = self.open_owner4()
        pk.openhow = self.openflag4()
        pk.claim = self.open_claim4()
        return pk

    def open_read_delegation4(self):
        pk = Pack('open_read_delegation4')
        pk.stateid = self.stateid4()
        pk.recall = self.bool()
        pk.permissions = self.nfsace4()
        return pk

    def open_write_delegation4(self):
        pk = Pack('open_write_delegation4')
        pk.stateid = self.stateid4()
        pk.recall = self.bool()
        pk.space_limit = self.nfs_space_limit4()
        pk.permissions = self.nfsace4()
        return pk

    def OPEN4resok(self):
        pk = Pack('OPEN4resok')
        pk.stateid = self.stateid4()
        pk.cinfo = self.change_info4()
        pk.rflags = self.uint32_t()
        pk.attrset = self.bitmap4()
        pk.delegation = self.open_delegation4()
        return pk

    def OPENATTR4args(self):
        pk = Pack('OPENATTR4args')
        pk.createdir = self.bool()
        return pk

    def OPENATTR4res(self):
        pk = Pack('OPENATTR4res')
        pk.status = self.nfsstat4()
        return pk

    def OPEN_CONFIRM4args(self):
        pk = Pack('OPEN_CONFIRM4args')
        pk.open_stateid = self.stateid4()
        pk.seqid = self.seqid4()
        return pk

    def OPEN_CONFIRM4resok(self):
        pk = Pack('OPEN_CONFIRM4resok')
        pk.open_stateid = self.stateid4()
        return pk

    def OPEN_DOWNGRADE4args(self):
        pk = Pack('OPEN_DOWNGRADE4args')
        pk.open_stateid = self.stateid4()
        pk.seqid = self.seqid4()
        pk.share_access = self.uint32_t()
        pk.share_deny = self.uint32_t()
        return pk

    def OPEN_DOWNGRADE4resok(self):
        pk = Pack('OPEN_DOWNGRADE4resok')
        pk.open_stateid = self.stateid4()
        return pk

    def PUTFH4args(self):
        pk = Pack('PUTFH4args')
        pk.object = self.nfs_fh4()
        return pk

    def PUTFH4res(self):
        pk = Pack('PUTFH4res')
        pk.status = self.nfsstat4()
        return pk

    def PUTPUBFH4res(self):
        pk = Pack('PUTPUBFH4res')
        pk.status = self.nfsstat4()
        return pk

    def PUTROOTFH4res(self):
        pk = Pack('PUTROOTFH4res')
        pk.status = self.nfsstat4()
        return pk

    def READ4args(self):
        pk = Pack('READ4args')
        pk.stateid = self.stateid4()
        pk.offset = self.offset4()
        pk.count = self.count4()
        return pk

    def READ4resok(self):
        pk = Pack('READ4resok')
        pk.eof = self.bool()
        pk.data = self.opaque(limit=None)
        return pk

    def READDIR4args(self):
        pk = Pack('READDIR4args')
        pk.cookie = self.nfs_cookie4()
        pk.cookieverf = self.verifier4()
        pk.dircount = self.count4()
        pk.maxcount = self.count4()
        pk.attr_request = self.bitmap4()
        return pk

    def entry4(self):
        pk = Pack('entry4')
        pk.cookie = self.nfs_cookie4()
        pk.name = self.component4()
        pk.attrs = self.fattr4()
        # recursive entry4 *nextentry 
        pk.nextentry = self._array(self.entry4)
        return pk

    def dirlist4(self):
        pk = Pack('dirlist4')
        # recursive entry4 *entries 
        pk.entries = self._array(self.entry4)
        pk.eof = self.bool()
        return pk

    def READDIR4resok(self):
        pk = Pack('READDIR4resok')
        pk.cookieverf = self.verifier4()
        pk.reply = self.dirlist4()
        return pk

    def READLINK4resok(self):
        pk = Pack('READLINK4resok')
        pk.link = self.linktext4()
        return pk

    def REMOVE4args(self):
        pk = Pack('REMOVE4args')
        pk.target = self.component4()
        return pk

    def REMOVE4resok(self):
        pk = Pack('REMOVE4resok')
        pk.cinfo = self.change_info4()
        return pk

    def RENAME4args(self):
        pk = Pack('RENAME4args')
        pk.oldname = self.component4()
        pk.newname = self.component4()
        return pk

    def RENAME4resok(self):
        pk = Pack('RENAME4resok')
        pk.source_cinfo = self.change_info4()
        pk.target_cinfo = self.change_info4()
        return pk

    def RENEW4args(self):
        pk = Pack('RENEW4args')
        pk.clientid = self.clientid4()
        return pk

    def RENEW4res(self):
        pk = Pack('RENEW4res')
        pk.status = self.nfsstat4()
        return pk

    def RESTOREFH4res(self):
        pk = Pack('RESTOREFH4res')
        pk.status = self.nfsstat4()
        return pk

    def SAVEFH4res(self):
        pk = Pack('SAVEFH4res')
        pk.status = self.nfsstat4()
        return pk

    def SECINFO4args(self):
        pk = Pack('SECINFO4args')
        pk.name = self.component4()
        return pk

    def rpcsec_gss_info(self):
        pk = Pack('rpcsec_gss_info')
        pk.oid = self.sec_oid4()
        pk.qop = self.qop4()
        pk.service = self.rpc_gss_svc_t()
        return pk

    def SETATTR4args(self):
        pk = Pack('SETATTR4args')
        pk.stateid = self.stateid4()
        pk.obj_attributes = self.fattr4()
        return pk

    def SETATTR4res(self):
        pk = Pack('SETATTR4res')
        pk.status = self.nfsstat4()
        pk.attrsset = self.bitmap4()
        return pk

    def SETCLIENTID4args(self):
        pk = Pack('SETCLIENTID4args')
        pk.client = self.nfs_client_id4()
        pk.callback = self.cb_client4()
        pk.callback_ident = self.uint32_t()
        return pk

    def SETCLIENTID4resok(self):
        pk = Pack('SETCLIENTID4resok')
        pk.clientid = self.clientid4()
        pk.setclientid_confirm = self.verifier4()
        return pk

    def SETCLIENTID_CONFIRM4args(self):
        pk = Pack('SETCLIENTID_CONFIRM4args')
        pk.clientid = self.clientid4()
        pk.setclientid_confirm = self.verifier4()
        return pk

    def SETCLIENTID_CONFIRM4res(self):
        pk = Pack('SETCLIENTID_CONFIRM4res')
        pk.status = self.nfsstat4()
        return pk

    def VERIFY4args(self):
        pk = Pack('VERIFY4args')
        pk.obj_attributes = self.fattr4()
        return pk

    def VERIFY4res(self):
        pk = Pack('VERIFY4res')
        pk.status = self.nfsstat4()
        return pk

    def WRITE4args(self):
        pk = Pack('WRITE4args')
        pk.stateid = self.stateid4()
        pk.offset = self.offset4()
        pk.stable = self.stable_how4()
        pk.data = self.opaque(limit=None)
        return pk

    def WRITE4resok(self):
        pk = Pack('WRITE4resok')
        pk.count = self.count4()
        pk.committed = self.stable_how4()
        pk.writeverf = self.verifier4()
        return pk

    def RELEASE_LOCKOWNER4args(self):
        pk = Pack('RELEASE_LOCKOWNER4args')
        pk.lock_owner = self.lock_owner4()
        return pk

    def RELEASE_LOCKOWNER4res(self):
        pk = Pack('RELEASE_LOCKOWNER4res')
        pk.status = self.nfsstat4()
        return pk

    def ILLEGAL4res(self):
        pk = Pack('ILLEGAL4res')
        pk.status = self.nfsstat4()
        return pk

    def CB_COMPOUND4args(self):
        pk = Pack('CB_COMPOUND4args')
        pk.tag = self.utf8str_cs()
        pk.minorversion = self.uint32_t()
        pk.callback_ident = self.uint32_t()
        pk.argarray = self._array(self.nfs_cb_argop4,limit=None)
        return pk

    def CB_COMPOUND4res(self):
        pk = Pack('CB_COMPOUND4res')
        pk.status = self.nfsstat4()
        pk.tag = self.utf8str_cs()
        pk.resarray = self._array(self.nfs_cb_resop4,limit=None)
        return pk

    def CB_GETATTR4args(self):
        pk = Pack('CB_GETATTR4args')
        pk.fh = self.nfs_fh4()
        pk.attr_request = self.bitmap4()
        return pk

    def CB_GETATTR4resok(self):
        pk = Pack('CB_GETATTR4resok')
        pk.obj_attributes = self.fattr4()
        return pk

    def CB_RECALL4args(self):
        pk = Pack('CB_RECALL4args')
        pk.stateid = self.stateid4()
        pk.truncate = self.bool()
        pk.fh = self.nfs_fh4()
        return pk

    def CB_RECALL4res(self):
        pk = Pack('CB_RECALL4res')
        pk.status = self.nfsstat4()
        return pk

    def CB_ILLEGAL4res(self):
        pk = Pack('CB_ILLEGAL4res')
        pk.status = self.nfsstat4()
        return pk

    def settime4(self):
        pk = Pack('settime4')
        pk.set_it = self.time_how4()
        if pk.set_it in [const.SET_TO_CLIENT_TIME4]:
            pk.time = self.nfstime4()
        return pk
    def ACCESS4res(self):
        pk = Pack('ACCESS4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.ACCESS4resok()
        return pk
    def CLOSE4res(self):
        pk = Pack('CLOSE4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.open_stateid = self.stateid4()
        return pk
    def COMMIT4res(self):
        pk = Pack('COMMIT4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.COMMIT4resok()
        return pk
    def createtype4(self):
        pk = Pack('createtype4')
        pk.type = self.nfs_ftype4()
        if pk.type in [const.NF4LNK]:
            pk.linkdata = self.linktext4()
        elif pk.type in [const.NF4BLK,const.NF4CHR]:
            pk.devdata = self.specdata4()
        return pk
    def CREATE4res(self):
        pk = Pack('CREATE4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.CREATE4resok()
        return pk
    def GETATTR4res(self):
        pk = Pack('GETATTR4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.GETATTR4resok()
        return pk
    def GETFH4res(self):
        pk = Pack('GETFH4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.GETFH4resok()
        return pk
    def LINK4res(self):
        pk = Pack('LINK4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.LINK4resok()
        return pk
    def locker4(self):
        pk = Pack('locker4')
        pk.new_lock_owner = self.bool()
        if pk.new_lock_owner in [const.TRUE]:
            pk.open_owner = self.open_to_lock_owner4()
        elif pk.new_lock_owner in [const.FALSE]:
            pk.lock_owner = self.exist_lock_owner4()
        return pk
    def LOCK4res(self):
        pk = Pack('LOCK4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.LOCK4resok()
        elif pk.status in [const.NFS4ERR_DENIED]:
            pk.denied = self.LOCK4denied()
        return pk
    def LOCKT4res(self):
        pk = Pack('LOCKT4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4ERR_DENIED]:
            pk.denied = self.LOCK4denied()
        return pk
    def LOCKU4res(self):
        pk = Pack('LOCKU4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.lock_stateid = self.stateid4()
        return pk
    def createhow4(self):
        pk = Pack('createhow4')
        pk.mode = self.createmode4()
        if pk.mode in [const.UNCHECKED4,const.GUARDED4]:
            pk.createattrs = self.fattr4()
        elif pk.mode in [const.EXCLUSIVE4]:
            pk.createverf = self.verifier4()
        return pk
    def openflag4(self):
        pk = Pack('openflag4')
        pk.opentype = self.opentype4()
        if pk.opentype in [const.OPEN4_CREATE]:
            pk.how = self.createhow4()
        return pk
    def nfs_space_limit4(self):
        pk = Pack('nfs_space_limit4')
        pk.limitby = self.limit_by4()
        if pk.limitby in [const.NFS_LIMIT_SIZE]:
            pk.filesize = self.uint64_t()
        elif pk.limitby in [const.NFS_LIMIT_BLOCKS]:
            pk.mod_blocks = self.nfs_modified_limit4()
        return pk
    def open_claim4(self):
        pk = Pack('open_claim4')
        pk.claim = self.open_claim_type4()
        if pk.claim in [const.CLAIM_NULL]:
            pk.file = self.component4()
        elif pk.claim in [const.CLAIM_PREVIOUS]:
            pk.delegate_type = self.open_delegation_type4()
        elif pk.claim in [const.CLAIM_DELEGATE_CUR]:
            pk.delegate_cur_info = self.open_claim_delegate_cur4()
        elif pk.claim in [const.CLAIM_DELEGATE_PREV]:
            pk.file_delegate_prev = self.component4()
        return pk
    def open_delegation4(self):
        pk = Pack('open_delegation4')
        pk.delegation_type = self.open_delegation_type4()
        if pk.delegation_type in [const.OPEN_DELEGATE_READ]:
            pk.read = self.open_read_delegation4()
        elif pk.delegation_type in [const.OPEN_DELEGATE_WRITE]:
            pk.write = self.open_write_delegation4()
        return pk
    def OPEN4res(self):
        pk = Pack('OPEN4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.OPEN4resok()
        return pk
    def OPEN_CONFIRM4res(self):
        pk = Pack('OPEN_CONFIRM4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.OPEN_CONFIRM4resok()
        return pk
    def OPEN_DOWNGRADE4res(self):
        pk = Pack('OPEN_DOWNGRADE4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.OPEN_DOWNGRADE4resok()
        return pk
    def READ4res(self):
        pk = Pack('READ4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.READ4resok()
        return pk
    def READDIR4res(self):
        pk = Pack('READDIR4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.READDIR4resok()
        return pk
    def READLINK4res(self):
        pk = Pack('READLINK4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.READLINK4resok()
        return pk
    def REMOVE4res(self):
        pk = Pack('REMOVE4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.REMOVE4resok()
        return pk
    def RENAME4res(self):
        pk = Pack('RENAME4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.RENAME4resok()
        return pk
    def secinfo4(self):
        pk = Pack('secinfo4')
        pk.flavor = self.uint32_t()
        if pk.flavor in [const.RPCSEC_GSS]:
            pk.flavor_info = self.rpcsec_gss_info()
        return pk
    def SECINFO4res(self):
        pk = Pack('SECINFO4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.SECINFO4resok()
        return pk
    def SETCLIENTID4res(self):
        pk = Pack('SETCLIENTID4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.SETCLIENTID4resok()
        elif pk.status in [const.NFS4ERR_CLID_INUSE]:
            pk.client_using = self.clientaddr4()
        return pk
    def WRITE4res(self):
        pk = Pack('WRITE4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.WRITE4resok()
        return pk
    def nfs_cb_argop4(self):
        pk = Pack('nfs_cb_argop4')
        pk.argop = self.unsigned()
        if pk.argop in [const.OP_CB_GETATTR]:
            pk.opcbgetattr = self.CB_GETATTR4args()
        elif pk.argop in [const.OP_CB_RECALL]:
            pk.opcbrecall = self.CB_RECALL4args()
        return pk
    def nfs_cb_resop4(self):
        pk = Pack('nfs_cb_resop4')
        pk.resop = self.unsigned()
        if pk.resop in [const.OP_CB_GETATTR]:
            pk.opcbgetattr = self.CB_GETATTR4res()
        elif pk.resop in [const.OP_CB_RECALL]:
            pk.opcbrecall = self.CB_RECALL4res()
        elif pk.resop in [const.OP_CB_ILLEGAL]:
            pk.opcbillegal = self.CB_ILLEGAL4res()
        return pk
    def CB_GETATTR4res(self):
        pk = Pack('CB_GETATTR4res')
        pk.status = self.nfsstat4()
        if pk.status in [const.NFS4_OK]:
            pk.resok4 = self.CB_GETATTR4resok()
        return pk
