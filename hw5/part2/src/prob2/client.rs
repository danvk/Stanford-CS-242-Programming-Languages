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

// The ids sent method should be accessible from all states besides the Client state and
// should return ids, the ids of all the packets that have been sent by the client and
// successfully received by a server since the most recent Initial state -
// if a client moves from Closed to Initial, it should behave like a fresh client
// that has not sent any packets.
//
// The order of ids in ids is unimportant.

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
            Some(Sig::SynAck) => Ok(Syned {}),
            _ => Err(self),
        }
    }
    pub fn ids_sent(&self) -> Vec<u32> {
        vec![]
    }
}

pub struct Syned {}
impl Syned {
    pub fn send_ack(self, server: &mut Server) -> SynAcked {
        _ = internal_send_sig(server, Sig::Ack);
        SynAcked { pkts_received: vec![] }
    }
    pub fn ids_sent(&self) -> Vec<u32> {
        vec![]
    }
}

pub struct SynAcked {
    pkts_received: Vec<u32>,
}
impl SynAcked {
    pub fn send_pkts(self, server: &mut Server, pkts: &Vec<Pkt>) -> SynAcked {
        let mut new_pkts = internal_send_pkts(server, pkts);
        new_pkts.extend(self.pkts_received);
        SynAcked { pkts_received: new_pkts }
    }
    pub fn send_close(self, server: &mut Server) -> Result<Closed, SynAcked> {
        let result = internal_send_sig(server, Sig::Close);
        match result {
            Some(Sig::CloseAck) => Ok(Closed { pkts_received: self.pkts_received }),
            _ => Err(self),
        }
    }
    pub fn ids_sent(&self) -> Vec<u32> {
        self.pkts_received.clone()
    }
}

pub struct Closed {
    pkts_received: Vec<u32>,
}
impl Closed {
    pub fn send_ack(self, server: &mut Server) -> Initial {
        _ = internal_send_sig(server, Sig::Ack);
        Initial {}
    }
    pub fn ids_sent(&self) -> Vec<u32> {
        self.pkts_received.clone()
    }
}
//===== END_CODE =====//
