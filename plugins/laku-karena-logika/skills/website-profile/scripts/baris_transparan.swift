// Daftar rentang baris berisi/kosong pada PNG transparan: swift baris_transparan.swift <gambar.png>
import AppKit
let img = NSImage(contentsOfFile: CommandLine.arguments[1])!
let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
let w = rep.pixelsWide, h = rep.pixelsHigh
var runs: [(Int,Bool)] = []
var prev: Bool? = nil
for y in 0..<h {
  var any = false
  var x = 0
  while x < w { if rep.colorAt(x: x, y: y)!.alphaComponent > 0.05 { any = true; break }; x += 3 }
  if any != prev { runs.append((y, any)); prev = any }
}
print(w, h); for r in runs { print(r.0, r.1 ? "isi" : "kosong") }
// kolom bbox untuk baris 0..<split
