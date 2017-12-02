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
pub extern fn get_code_1() -> String {
    let filename = "code1.txt";
    let mut f = File::open(filename).expect("file not found");
    let mut contents = String::new();
    f.read_to_string(&mut contents)
        .expect("something went wrong reading the file");

    contents.pop();
    return contents;
}

#[no_mangle]
pub extern fn get_code_2() -> String {
    let filename = "code2.txt";
    let mut f = File::open(filename).expect("file not found");
    let mut contents = String::new();
    f.read_to_string(&mut contents)
        .expect("something went wrong reading the file");

    contents.pop();
    return contents;
}

#[no_mangle]
pub extern fn get_detonation_code(code_1: &str, code_2: &str) -> i64 {
    let r_code_1 = get_code_1();
    let r_code_2 = get_code_2();
    println!("{} --- {}", r_code_1, r_code_2);
    println!("{} --- {}", code_1, code_2);
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
    println!("Nope");
    return 0;
}

#[no_mangle]
pub extern fn set_detonation_code(note_id: u64, token: &str) -> u64 {
    println!("OK");
    println!("{} --- {}", note_id, token);
    return 0;
}

#[no_mangle]
pub extern fn get_flag(s: &str, s2: &str) {
    println!("{}", s);
    println!("{}", s2);
}