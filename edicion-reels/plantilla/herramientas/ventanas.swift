import CoreGraphics
let l = CGWindowListCopyWindowInfo([.optionOnScreenOnly], kCGNullWindowID) as! [[String: Any]]
for w in l where (w["kCGWindowLayer"] as? Int) == 0 {
  let b = w["kCGWindowBounds"] as! [String: Any]
  print(w["kCGWindowNumber"]!, w["kCGWindowOwnerName"] ?? "", w["kCGWindowName"] ?? "", b["X"]!, b["Y"]!, b["Width"]!, b["Height"]!)
}
