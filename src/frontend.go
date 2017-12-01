package main

import "os"
import "unsafe"

//go:cgo_import_static check_core
//go:cgo_import_static increment
//go:cgo_import_static hello
//go:linkname _hello hello
//go:linkname _check_core check_core 

/* ----- IMPORTED SYMBOLS ADDR ----- */

var _hello byte
var hello = unsafe.Pointer(&_hello)

var _check_core byte
var check_core = unsafe.Pointer(&_check_core)

/* ----- TRAMPOLINE ----- */

func trampoline(arg unsafe.Pointer) uint64
func exploit()


func main() {
    println(hello)
    if len(os.Args) != 2 {
        println("Houston we have a problem")
        return
    }
    routine := os.Args[1]
    switch routine {
    case "check_core":
        println("caso 1")
        trampoline(check_core)
    case "trampoline":
        println("caso 2")
        println(trampoline(hello))
    case "exploit":
        println("caso 3")
        exploit()
    default:
        println("Houston we have another problem")
    }
}