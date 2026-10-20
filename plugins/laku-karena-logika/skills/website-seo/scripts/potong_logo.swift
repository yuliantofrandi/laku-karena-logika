// Potong logo PNG transparan (mis. buang tagline) + perkecil: swift potong_logo.swift <masuk.png> <keluar.png> <batas_bawah_px> <tinggi_keluar>
// batas_bawah_px = baris terakhir wordmark (cari baris transparan pemisah dengan baris_transparan.swift). tinggi_keluar = 3× tinggi tampil.
import AppKit
let A = CommandLine.arguments
let src = NSBitmapImageRep(data: NSImage(contentsOfFile: A[1])!.tiffRepresentation!)!
let H = Int(A[3])!, outH = Int(A[4])!
let w = src.pixelsWide
var minX = w, maxX = 0, minY = H, maxY = 0
for y in stride(from: 0, to: H, by: 2) { for x in stride(from: 0, to: w, by: 2) {
  if src.colorAt(x: x, y: y)!.alphaComponent > 0.05 { minX = min(minX,x); maxX = max(maxX,x); minY = min(minY,y); maxY = max(maxY,y) } } }
minX = max(0, minX-2); minY = max(0, minY-2); maxX = min(w-1, maxX+2); maxY = min(H-1, maxY+2)
let cw = maxX-minX+1, ch = maxY-minY+1
let cg = src.cgImage!.cropping(to: CGRect(x: minX, y: minY, width: cw, height: ch))!
let outW = Int((Double(cw) * Double(outH) / Double(ch)).rounded())
let ctx = CGContext(data: nil, width: outW, height: outH, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.interpolationQuality = .high
ctx.draw(cg, in: CGRect(x: 0, y: 0, width: outW, height: outH))
let png = NSBitmapImageRep(cgImage: ctx.makeImage()!).representation(using: .png, properties: [:])!
try! png.write(to: URL(fileURLWithPath: A[2]))
print(cw, ch, "->", outW, outH)
