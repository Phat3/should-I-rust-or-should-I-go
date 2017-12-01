package main

import "os"
import "unsafe"

//go:cgo_import_static check_core
//go:cgo_import_static increment
//go:cgo_import_static hello
//go:cgo_import_static get_detonation_code
//go:cgo_import_static get_code_1
//go:cgo_import_static get_code_2
//go:linkname _hello hello
//go:linkname _check_core check_core
//go:linkname _get_detonation_code get_detonation_code

/* ----- IMPORTED SYMBOLS ADDR ----- */

var _hello byte
var hello = unsafe.Pointer(&_hello)

var _check_core byte
var check_core = unsafe.Pointer(&_check_core)

var _get_detonation_code byte
var get_detonation_code = unsafe.Pointer(&_get_detonation_code)

/* ----- TRAMPOLINE ----- */

func trampoline(arg unsafe.Pointer)
func callGetDetonationCode(arg unsafe.Pointer, arg2, arg3 int) int
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
		trampoline(hello)
	case "detonation":
		println("DETONATION")
		println(callGetDetonationCode(get_detonation_code, 10, 20))
	case "exploit":
		println("caso 3")
		exploit()
	default:
		println("Houston we have another problem")
	}
}
