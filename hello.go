package main

//go:cgo_import_static hello
func trampoline()

func main() {
    println("Hello go!")
    trampoline()
}
