extern crate part1;
#[allow(unused_imports)]
use part1::prob1::cart::Cart;

fn main() {
    match Cart::login("id1".to_string(), "pw1".to_string()) {
        Err(()) =>
            assert!(false),
        Ok(empty) => {
            let cart = empty.add_item(10).add_item(32).checkout();
            // add_item should be inaccessible from Checkout state
            cart.add_item(32);
        }
    }
}
