package main

import (
	"os"
	"strconv"
	"unsafe"
)

//go:cgo_import_static check_core
//go:cgo_import_static get_detonation_code
//go:cgo_import_static set_detonation_code
//go:cgo_import_static set_variable_yield
//go:cgo_import_static set_dt_amount
//go:cgo_import_static toggle_eni
//go:cgo_import_static defuse
//go:cgo_import_static get_token
//go:cgo_import_static set_token
//go:linkname _check_core check_core
//go:linkname _get_detonation_code get_detonation_code
//go:linkname _set_detonation_code set_detonation_code
//go:linkname _set_variable_yield set_variable_yield
//go:linkname _set_dt_amount set_dt_amount
//go:linkname _toggle_eni toggle_eni
//go:linkname _defuse defuse

/* ----- IMPORTED SYMBOLS ADDR ----- */

var _check_core byte
var check_core = unsafe.Pointer(&_check_core)

var _set_variable_yield byte
var set_variable_yield = unsafe.Pointer(&_set_variable_yield)

var _set_dt_amount byte
var set_dt_amount = unsafe.Pointer(&_set_dt_amount)

var _toggle_eni byte
var toggle_eni = unsafe.Pointer(&_toggle_eni)

var _defuse byte
var defuse = unsafe.Pointer(&_defuse)

/* ----- TRAMPOLINES ----- */

func callCheckCore(arg unsafe.Pointer)
func callSetVariableYield(arg unsafe.Pointer, arg2 int)
func callSetDtAmount(arg unsafe.Pointer, arg2 int)
func callToggleEni(arg unsafe.Pointer)
func callDefuse(arg unsafe.Pointer, arg2 int, arg3 string, arg4 int)
func custom()

func main() {
	if len(os.Args) < 2 {
		println("Houston we have a problem")
		return
	}
	routine := os.Args[1]
	switch routine {
	case "check_core":
		callCheckCore(check_core)
	case "set_variable_yield":
		amount, _ := strconv.Atoi(os.Args[2])
		callSetVariableYield(set_variable_yield, amount)
	case "set_dt_amount":
		amount, _ := strconv.Atoi(os.Args[2])
		callSetDtAmount(set_dt_amount, amount)
	case "toggle_eni":
		callToggleEni(toggle_eni)
	case "defuse":
		id, _ := strconv.Atoi(os.Args[2])
		callDefuse(defuse, id, os.Args[3], len(os.Args[3]))
	default:
		custom()
	}
}
