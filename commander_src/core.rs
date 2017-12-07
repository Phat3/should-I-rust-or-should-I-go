#![crate_type = "staticlib"]

use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

static mut BOMB_TYPE: &str = "Teller-Ulam";
static mut VARIABLE_YIELD: u64 = 800000000;
static mut DT_AMOUNT: u64 = 25;
static mut USE_ENI: bool = true;

#[no_mangle]
pub extern fn check_core() {
    unsafe{
        println!("-------------------------------- INFO --------------------------------");
        println!("Type: {}", BOMB_TYPE);
        println!("Variable Yield: {} gigatons", VARIABLE_YIELD);
        println!("Deuterium / Tritium percentage in fission stage: {}%", DT_AMOUNT);
        println!("Use External Neutron Initiator: {}", USE_ENI);
        println!("----------------------------------------------------------------------");
    }
}

#[no_mangle]
pub extern fn set_variable_yield(var_yield: u64) {
    unsafe{
        VARIABLE_YIELD = var_yield;
        println!("New variable yield: {}", VARIABLE_YIELD);
    }
}

#[no_mangle]
pub extern fn set_dt_amount(dt_amo: u64) {
    unsafe{
        if dt_amo > 100 {
            println!("You skipped some math lesson uh... Maybe someone got laid too much in college eh...");
        }
        DT_AMOUNT = dt_amo;
        println!("New Deterium / Tritium percentage: {}", DT_AMOUNT);
    }
}

#[no_mangle]
pub extern fn toggle_eni() {
    unsafe{
        USE_ENI = if USE_ENI == true { false } else { true };
        println!("External Neutron Initiator Toggled");
    }
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

#[no_mangle]
pub extern fn defuse(id: u64, token: &str) -> i64 {
    unsafe{
        let filename = format!("{}_token.txt", id);
        let path = Path::new(&filename);
        if path.exists() && token == get_token(id){
            println!("{} bomb defused\n", BOMB_TYPE);
            println!("Well I would say to you 'good job, you saved humanity!' but you know my philosophy:");
            println!("Nobody exists on purpose. Nobody belongs anywhere. We're all going to die. Come watch TV!");
        }
        else{
            println!("Don't even trip dawg");
        }
    }
    return 0;
}