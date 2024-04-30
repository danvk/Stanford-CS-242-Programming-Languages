extern crate part1;
#[allow(unused_imports)]
use part1::prob1::cart::Cart;

fn main() {
    match Cart::login("id1".to_string(), "pw1".to_string()) {
        Err(()) =>
            assert!(false),
        Ok(empty) => {
            let cart1 = empty.add_item(10);
            let _cart2 = cart1.add_item(11);
            // cart1 should be inaccessible after adding to it.
            let _cart3 = cart1.add_item(12);
        }
    }
}
