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
pub extern fn get_code_1() -> i64 {
    return 10;
}

#[no_mangle]
pub extern fn get_code_2() -> i64 {
    return 20;
}

#[no_mangle]
pub extern fn get_detonation_code(code_1: i64, code_2: i64) -> i64 {
    if code_1 == get_code_1() && code_2 == get_code_2() {
        println!("Entrato");
        return 1;
        /*
        let filename = "secret.txt";

        let mut f = File::open(filename).expect("file not found");

        let mut contents = String::new();
        f.read_to_string(&mut contents)
            .expect("something went wrong reading the file");

        println!("{}", contents);
        */
    }
    println!("{} --- {}", code_1, code_2);
    println!("Nope");
    return 0;
}