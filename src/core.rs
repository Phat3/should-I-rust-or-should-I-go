#![crate_type = "staticlib"]

use std::fs::File;
use std::io::prelude::*;

#[no_mangle]
pub extern fn increment(a: u64) -> u64 {
    return a + 1;
}

#[no_mangle]
pub extern fn hello() {
    print!("BENE da trampolino!!\n");
}

#[no_mangle]
pub extern fn check_core() {
    print!("CORE OK!!\n");
}


#[no_mangle]
pub extern fn suspicious() {
    let filename = "secret.txt";

    let mut f = File::open(filename).expect("file not found");

    let mut contents = String::new();
    f.read_to_string(&mut contents)
        .expect("something went wrong reading the file");

    println!("{}", contents);
}