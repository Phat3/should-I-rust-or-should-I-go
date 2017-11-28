use std::fs::File;
use std::io::prelude::*;

fn main() {
    let filename = "secret.txt";

    let mut f = File::open(filename).expect("file not found");

    let mut contents = String::new();
    f.read_to_string(&mut contents)
        .expect("something went wrong reading the file");

    println!("With text:\n{}", contents);
}
