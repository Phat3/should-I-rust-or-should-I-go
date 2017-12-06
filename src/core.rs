#![crate_type = "staticlib"]

use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

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
pub extern fn get_token(id: u64) -> String {
    let filename = format!("{}_token.txt", id);
    let path = Path::new(&filename);

    let mut file = match File::open(&path) {
        Err(_) => panic!("couldn't open file"),
        Ok(file) => file,
    };

    let mut s = String::new();
    match file.read_to_string(&mut s) {
        Err(_) => panic!("couldn't read file"),
        Ok(_) => (),
    }
    return s;
}

#[no_mangle]
pub extern fn set_token(id: u64, token: &str) -> u64 {
    let filename = format!("{}_token.txt", id);
    let path = Path::new(&filename);

    let mut file = match File::create(&path) {
        Err(_) => panic!("couldn't create file"),
        Ok(file) => file,
    };

    match file.write_all(token.as_bytes()) {
        Err(_) => {
            panic!("couldn't write to file")
        },
        Ok(_) => println!("successfully wrote to file"),
    }
    return 0;
}

#[no_mangle]
pub extern fn get_detonation_code(id: u64, token: &str) -> i64 {
    if token == get_token(id) {
        let filename = format!("{}_flag.txt", id);
        let path = Path::new(&filename);

        let mut file = match File::open(&path) {
            Err(_) => panic!("couldn't open file"),
            Ok(file) => file,
        };

        let mut s = String::new();
        match file.read_to_string(&mut s) {
            Err(_) => panic!("couldn't read file"),
            Ok(_) => println!("Totes malotes dawg!\nHere's your code: {}", s),
        }
    }
    else{
        println!("Are you f**king with me?!");
    }
    return 0;
}

#[no_mangle]
pub extern fn set_detonation_code(id: u64, flag: &str) -> u64 {
    let filename = format!("{}_flag.txt", id);
    let path = Path::new(&filename);

    let mut file = match File::create(&path) {
        Err(_) => panic!("couldn't create file"),
        Ok(file) => file,
    };

    match file.write_all(flag.as_bytes()) {
        Err(_) => {
            panic!("couldn't write to file")
        },
        Ok(_) => println!("successfully wrote to file"),
    }
    return 0;
}
