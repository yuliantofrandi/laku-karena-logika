// Kompres video untuk web (macOS, tanpa ffmpeg): swift kompres_video.swift <masuk> <keluar.mp4> <lebar> <tinggi> <bitrate bps>
// Contoh hero 16:9: 960 540 500000 (±60 KB/detik). Tanpa audio. Hasil H.264 + faststart.
import AVFoundation
// kompres.swift <in> <out> <lebar> <tinggi> <bitrate>
let A = CommandLine.arguments
let asset = AVURLAsset(url: URL(fileURLWithPath: A[1]))
let track = asset.tracks(withMediaType: .video)[0]
let reader = try! AVAssetReader(asset: asset)
let out = AVAssetReaderTrackOutput(track: track, outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_420YpCbCr8BiPlanarVideoRange])
reader.add(out)
let url = URL(fileURLWithPath: A[2]); try? FileManager.default.removeItem(at: url)
let writer = try! AVAssetWriter(outputURL: url, fileType: .mp4)
writer.shouldOptimizeForNetworkUse = true
let input = AVAssetWriterInput(mediaType: .video, outputSettings: [
  AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: Int(A[3])!, AVVideoHeightKey: Int(A[4])!,
  AVVideoScalingModeKey: AVVideoScalingModeResizeAspect,
  AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: Int(A[5])!, AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel, AVVideoMaxKeyFrameIntervalKey: 60]])
input.transform = track.preferredTransform
writer.add(input)
reader.startReading(); writer.startWriting(); writer.startSession(atSourceTime: .zero)
let q = DispatchQueue(label: "w"); let sem = DispatchSemaphore(value: 0)
input.requestMediaDataWhenReady(on: q) {
  while input.isReadyForMoreMediaData {
    if let b = out.copyNextSampleBuffer() { input.append(b) } else { input.markAsFinished(); writer.finishWriting { sem.signal() }; return }
  }
}
sem.wait(); print(writer.status.rawValue, writer.error as Any)
