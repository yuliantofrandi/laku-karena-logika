import Foundation
import Vision
import AppKit
let path = CommandLine.arguments[1]
guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { exit(1) }
let W = Double(cg.width), H = Double(cg.height)
let req = VNRecognizeTextRequest()
req.recognitionLevel = .accurate
req.usesLanguageCorrection = false
let faces = VNDetectFaceRectanglesRequest()
try VNImageRequestHandler(cgImage: cg, options: [:]).perform([req, faces])
for o in req.results ?? [] {
  guard let t = o.topCandidates(1).first else { continue }
  let b = o.boundingBox
  print(String(format: "T\t%d\t%d\t%d\t%d\t%@", Int(b.minX*W), Int((1-b.maxY)*H), Int(b.width*W), Int(b.height*H), t.string))
}
for f in faces.results ?? [] { let b = f.boundingBox
  print(String(format: "F\t%d\t%d\t%d\t%d", Int(b.minX*W), Int((1-b.maxY)*H), Int(b.width*W), Int(b.height*H))) }
