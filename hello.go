package main

//go:cgo_import_static increment
//go:cgo_import_static hello
//go:cgo_import_static suspicious
func trampoline()

func main() {
    println("Hello go!")
    trampoline()
}
