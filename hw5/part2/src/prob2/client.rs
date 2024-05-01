/***************
 * NOTE:
 *   You can use `Sig`, `Pkt`, ..., `internal_send_pkts`
 *   which appear in the below `use` declarations,
 *   simply by `Sig`, `Pkt`, ..., `internal_send_pkts` without any prefixes.
 ***************/

#[allow(unused_imports)]
use crate::prob2::msg::{Pkt, Sig};
#[allow(unused_imports)]
use crate::prob2::server::{internal_send_pkts, internal_send_sig, Server};

// TODO: Implement the typestate structs below for the TCP client. You are free to add any fields
// that you think will be helpful to the struct definitions.
// Below shows the signature of the methods needed across the TCP client state machine.
// Note that not all methods may be implemented for every typestate struct.
//
//   pub fn new() -> T
//   pub fn send_syn(self, _: &mut Server) -> Result<T,T>
//   pub fn send_ack(self, _: &mut Server) -> T
//   pub fn send_pkts(self, _: &mut Server, _: &Vec<Pkt>) -> T
//   pub fn send_close(self, _: &mut Server) -> Result<T,T>
//   pub fn ids_sent(&self) -> Vec<u32>
//
// Here T denotes a type. Note that each T can be a different type.
//===== BEGIN_CODE =====//
pub struct Client {}
impl Client {
    pub fn new() -> Initial {
        Initial {}
    }
}

pub struct Initial {}
impl Initial {
    pub fn send_syn(self, server: &mut Server) -> Result<Syned, Initial> {
        let result = internal_send_sig(server, Sig::Syn);
        match result {
            Some(syn_ret) => Ok(Syned {}),
            None => Err(self),
        }
    }
}

pub struct Syned {}
impl Syned {
    pub fn send_ack(self, server: &mut Server) -> SynAcked {
        _ = internal_send_sig(server, Sig::Ack);
        SynAcked {}
    }
}

pub struct SynAcked {}
pub struct Closed {}
//===== END_CODE =====//
