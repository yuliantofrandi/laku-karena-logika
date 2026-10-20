// Ambil frame poster: swift poster_video.swift <video> <awalan-keluar> <detik,detik,...> → <awalan>-<detik>.jpg
// Pilih frame yang informatif (bukan fade-in), lalu: sips -Z 960 -s format jpeg -s formatOptions 70 <frame>.jpg --out <poster>.jpg
import AVFoundation
import AppKit
let a = AVURLAsset(url: URL(fileURLWithPath: CommandLine.arguments[1]))
let g = AVAssetImageGenerator(asset: a)
g.appliesPreferredTrackTransform = true
g.requestedTimeToleranceBefore = .zero; g.requestedTimeToleranceAfter = .zero
for s in CommandLine.arguments[3].split(separator: ",").map({ Double($0)! }) {
  let cg = try! g.copyCGImage(at: CMTime(seconds: s, preferredTimescale: 600), actualTime: nil)
  let d = NSBitmapImageRep(cgImage: cg).representation(using: .jpeg, properties: [.compressionFactor: 0.75])!
  try! d.write(to: URL(fileURLWithPath: CommandLine.arguments[2] + "-\(s).jpg"))
}
