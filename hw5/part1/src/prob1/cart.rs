/***************
 * NOTE:
 *   You can call `internal_login` simply by `internal_login(id, pw)`.
 ***************/

#[allow(unused_imports)]
use crate::prob1::server::internal_login;

// TODO: Implement the following typestate structs. You are free to add any fields to the struct
// definitions.
// Below shows the signature of the methods to be implemented across the cart state machine.
// Note that not all methods may be implemented for every typestate struct.
//
//   pub fn login(_: String, _: String) -> Result<T,()>
//   pub fn add_item(self, _: u32) -> T
//   pub fn clear_items(self) -> T
//   pub fn checkout(self) -> T
//   pub fn cancel(self) -> T
//   pub fn order(self) -> T
//   pub fn acct_num(&self) -> u32
//   pub fn tot_cost(&self) -> u32
//
// Here T denotes a type. Note that each T can be a different type.
//===== BEGIN_CODE =====//
pub struct Cart {
}
impl Cart {
    pub fn login(id: String, pw: String) -> Result<Empty,()> {
        match internal_login(id, pw) {
            Some(account_num) => Ok(Empty {account_num}),
            None => Err(()),
        }
    }
}
pub struct Empty {
    account_num: u32,
}
impl Empty {
    pub fn add_item(self, item_cost: u32) -> NonEmpty {
        NonEmpty {
            account_num: self.account_num,
            total_cost: item_cost,
        }
    }
    pub fn acct_num(&self) -> u32 {
        self.account_num
    }
    pub fn tot_cost(&self) -> u32 {
        0
    }
}
pub struct NonEmpty {
    account_num: u32,
    total_cost: u32,
}
impl NonEmpty {
    pub fn add_item(self, item_cost: u32) -> NonEmpty {
        NonEmpty {
            account_num: self.account_num,
            total_cost: self.total_cost + item_cost,
        }
    }
    pub fn clear_items(self) -> Empty {
        Empty { account_num: self.account_num }
    }
    pub fn checkout(self) -> Checkout {
        Checkout { cart: self }
    }
    pub fn acct_num(&self) -> u32 {
        self.account_num
    }
    pub fn tot_cost(&self) -> u32 {
        self.total_cost
    }
}
pub struct Checkout {
    cart: NonEmpty,
}
impl Checkout {
    pub fn cancel(self) -> NonEmpty {
        self.cart
    }
    pub fn order(self) -> Empty {
        self.cart.clear_items()
    }
    pub fn acct_num(&self) -> u32 {
        self.cart.account_num
    }
    pub fn tot_cost(&self) -> u32 {
        self.cart.total_cost
    }
}

//===== END_CODE =====//
