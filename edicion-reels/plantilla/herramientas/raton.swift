import CoreGraphics
import Foundation
// raton drag x1 y1 x2 y2 | raton click x y
let a = CommandLine.arguments
func ev(_ t: CGEventType, _ x: Double, _ y: Double) { CGEvent(mouseEventSource: nil, mouseType: t, mouseCursorPosition: CGPoint(x: x, y: y), mouseButton: .left)?.post(tap: .cghidEventTap) }
let n = a.dropFirst(2).map { Double($0)! }
if a[1] == "click" { ev(.mouseMoved, n[0], n[1]); usleep(150000); ev(.leftMouseDown, n[0], n[1]); usleep(80000); ev(.leftMouseUp, n[0], n[1]) }
if a[1] == "drag" {
  ev(.mouseMoved, n[0], n[1]); usleep(200000); ev(.leftMouseDown, n[0], n[1]); usleep(400000)
  for i in 1...40 { let f = Double(i)/40; ev(.leftMouseDragged, n[0]+(n[2]-n[0])*f, n[1]+(n[3]-n[1])*f); usleep(25000) }
  usleep(400000); ev(.leftMouseUp, n[2], n[3])
}
