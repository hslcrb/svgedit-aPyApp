import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene, 
    QGraphicsItem, QGraphicsPathItem, QGraphicsItemGroup,
    QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QToolBar, QStatusBar, QColorDialog, QMenu
)
from PyQt6.QtGui import (
    QPainter, QPen, QBrush, QColor, QPainterPath, 
    QAction, QIcon, QCursor, QPixmap, QKeySequence
)


from PyQt6.QtCore import Qt, QRectF, QPointF, QSize
import svgelements as svg


class SVGCanvas(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent  # Store reference to main window
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setAcceptDrops(True)
        
        # Grid settings
        self.grid_size = 20
        self.draw_grid = True

    def drawBackground(self, painter, rect):
        if not self.draw_grid:
            super().drawBackground(painter, rect)
            return

        painter.setPen(QPen(QColor(40, 40, 40), 1))
        
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        
        for x in range(left, int(rect.right()), self.grid_size):
            painter.drawLine(x, int(rect.top()), x, int(rect.bottom()))
        for y in range(top, int(rect.bottom()), self.grid_size):
            painter.drawLine(int(rect.left()), y, int(rect.right()), y)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            fake_event = event
            super().mousePressEvent(fake_event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        
        menu = QMenu(self)
        
        if item:
            # item found
            if not item.isSelected():
                # If right-clicked item is not selected, select it exclusively
                self.scene.clearSelection()
                item.setSelected(True)
            
            export_action = menu.addAction("Export This Item")
            export_action.setIcon(IconProvider.get_icon("export"))
            try:
                export_action.triggered.connect(self.main_window.export_selected)
            except AttributeError:
                pass
            
            menu.addSeparator()
            
            try:
                group_action = menu.addAction("Group")
                group_action.setIcon(IconProvider.get_icon("group"))
                group_action.triggered.connect(self.main_window.group_selection)
                
                ungroup_action = menu.addAction("Ungroup")
                ungroup_action.setIcon(IconProvider.get_icon("ungroup"))
                ungroup_action.triggered.connect(self.main_window.ungroup_selection)
                
                menu.addSeparator()
                
                color_action = menu.addAction("Change Color")
                color_action.setIcon(IconProvider.get_icon("color"))
                color_action.triggered.connect(self.main_window.change_color)

                delete_action = menu.addAction("Delete")
                delete_action.setIcon(IconProvider.get_icon("delete", "#ff4444"))
                delete_action.triggered.connect(self.main_window.delete_selection)
            except AttributeError:
                pass
            
        else:
            # Empty space clicked
            paste_action = menu.addAction("Paste (Not Implemented)")
            paste_action.setEnabled(False)
            
        menu.exec(event.globalPos())



class IconProvider:
    @staticmethod
    def get_icon(name, color="#e0e0e0"):
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pen = QPen(QColor(color))
        pen.setWidth(4)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        if name == "open":
            # Folder icon
            painter.drawRoundedRect(4, 12, 56, 40, 4, 4)
            painter.drawLine(4, 12, 24, 12)
            painter.drawLine(24, 12, 28, 4)
            painter.drawLine(28, 4, 60, 4) # Top tab
            painter.drawLine(60, 4, 60, 12)
            
        elif name == "save":
            # Floppy diskish
            painter.drawRoundedRect(8, 8, 48, 48, 4, 4)
            painter.drawLine(16, 8, 16, 24)
            painter.drawLine(48, 8, 48, 24)
            painter.drawLine(16, 24, 48, 24) # Inner rect top
            painter.drawRect(20, 36, 24, 20) # Shutter
            
        elif name == "color":
            # Palette
            painter.setBrush(QBrush(QColor(color)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(8, 8, 48, 48)
            painter.setBrush(QBrush(QColor("#1e1e1e")))
            painter.drawEllipse(34, 16, 8, 8)
            painter.drawEllipse(44, 28, 8, 8)
            painter.drawEllipse(34, 40, 8, 8)
            painter.drawEllipse(20, 30, 8, 8)
            
        elif name == "group":
            # Box with items
            painter.drawRect(8, 8, 48, 48)
            painter.drawRect(16, 16, 12, 12)
            painter.drawRect(36, 16, 12, 12)
            painter.drawRect(16, 36, 12, 12)
            painter.drawRect(36, 36, 12, 12)
            
        elif name == "ungroup":
            # Separated items
            painter.drawRect(4, 4, 20, 20)
            painter.drawRect(40, 40, 20, 20)
            painter.drawRect(40, 4, 20, 20)
            pen.setStyle(Qt.PenStyle.DashLine)
            painter.setPen(pen)
            painter.drawRect(2, 2, 60, 60)
            
        elif name == "export":
            # Arrow up from tray
            painter.drawLine(10, 50, 54, 50)
            painter.drawLine(10, 50, 10, 40)
            painter.drawLine(54, 50, 54, 40)
            
            painter.drawLine(32, 10, 32, 40)
            painter.drawLine(32, 10, 18, 24)
            painter.drawLine(32, 10, 46, 24)
            
        elif name == "split":
            # 4 separate blocks
            painter.drawRect(4, 4, 24, 24)
            painter.drawRect(36, 4, 24, 24)
            painter.drawRect(4, 36, 24, 24)
            painter.drawRect(36, 36, 24, 24)
            
        elif name == "delete":
            # X mark
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawLine(16, 16, 48, 48)
            painter.drawLine(48, 16, 16, 48)
            
        elif name == "zoom_in":
            # Magnifying glass with +
            painter.drawEllipse(12, 12, 32, 32)
            painter.drawLine(36, 36, 52, 52)
            painter.drawLine(20, 28, 36, 28)
            painter.drawLine(28, 20, 28, 36)
            
        elif name == "zoom_out":
            # Magnifying glass with -
            painter.drawEllipse(12, 12, 32, 32)
            painter.drawLine(36, 36, 52, 52)
            painter.drawLine(20, 28, 36, 28)
            
        elif name == "zoom_fit":
            # Square with arrows pointing to corners
            painter.drawRoundedRect(16, 16, 32, 32, 4, 4)
            painter.drawLine(12, 12, 22, 12)
            painter.drawLine(12, 12, 12, 22)
            painter.drawLine(52, 52, 42, 52)
            painter.drawLine(52, 52, 52, 42)

        painter.end()
        return QIcon(pixmap)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SVG Master Pro - Advanced Editor")
        self.resize(1200, 800)
        self.current_file_path = None
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QToolBar {
                background-color: #2d2d2d;
                border-bottom: 1px solid #3d3d3d;
                spacing: 12px;
                padding: 6px;
            }
            QPushButton, QToolButton {
                background-color: transparent;
                color: #ffffff;
                border: none;
                padding: 6px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover, QToolButton:hover {
                background-color: #3d3d3d;
            }
            QToolButton::menu-indicator { 
                image: none; 
            }
            QMenu {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
            }
            QMenu::item {
                padding: 6px 24px;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
            QStatusBar {
                background-color: #2d2d2d;
                color: #888888;
            }
            QDockWidget {
                color: #ffffff;
                border: 1px solid #3d3d3d;
            }
            QDockWidget::title {
                background: #2d2d2d;
                padding: 6px;
                text-align: center;
            }
        """)

        self.canvas = SVGCanvas(self)
        self.setCentralWidget(self.canvas)

        self.setup_ui()

    def setup_ui(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(32, 32))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)


        # File Actions
        self.add_toolbar_action(toolbar, "Open", self.load_svg, "Open SVG File", "open")
        self.add_toolbar_action(toolbar, "Save", self.save_svg, "Save Entire Scene", "save")
        
        toolbar.addSeparator()

        # Edit Actions
        self.add_toolbar_action(toolbar, "Color", self.change_color, "Change Fill Color", "color")
        
        group_action = self.add_toolbar_action(toolbar, "Group", self.group_selection, "Group Selected (Ctrl+G)", "group")
        group_action.setShortcut("Ctrl+G")
        
        ungroup_action = self.add_toolbar_action(toolbar, "Ungroup", self.ungroup_selection, "Ungroup Selected (Ctrl+U)", "ungroup")
        ungroup_action.setShortcut("Ctrl+U")

        toolbar.addSeparator()

        # Export Action
        self.add_toolbar_action(toolbar, "Export", self.export_selected, "Export Selected to SVG", "export")
        self.add_toolbar_action(toolbar, "Split All", self.export_split_all, "Export All items as separate files", "split")

        toolbar.addSeparator()

        # View Actions
        zoom_in_action = self.add_toolbar_action(toolbar, "Zoom In", self.zoom_in, "Zoom In (Ctrl++)", "zoom_in")
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.setShortcutVisibleInContextMenu(True)
        
        zoom_out_action = self.add_toolbar_action(toolbar, "Zoom Out", self.zoom_out, "Zoom Out (Ctrl+-)", "zoom_out")
        zoom_out_action.setShortcut("Ctrl+-")
        
        reset_zoom_action = self.add_toolbar_action(toolbar, "Fit", self.reset_zoom, "Fit to Screen (Ctrl+0)", "zoom_fit")
        reset_zoom_action.setShortcut("Ctrl+0")

        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready")

        
        # Add Log Dock
        from PyQt6.QtWidgets import QDockWidget, QTextEdit
        self.log_dock = QDockWidget("Event Log", self)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background-color: #1e1e1e; color: #00ff00; font-family: monospace;")
        self.log_dock.setWidget(self.log_text)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.log_dock)

    def log_message(self, msg):
        self.log_text.append(msg)
        print(msg) # Also print to stdout

    def add_toolbar_action(self, toolbar, text, callback, tooltip, icon_name=None):
        action = QAction(text, self)
        if icon_name:
            action.setIcon(IconProvider.get_icon(icon_name))
        action.setToolTip(tooltip)
        action.triggered.connect(callback)
        toolbar.addAction(action)
        return action

    def change_color(self):
        items = self.canvas.scene.selectedItems()
        if not items:
            return
        
        color = QColorDialog.getColor()
        if color.isValid():
            for item in items:
                if isinstance(item, QGraphicsPathItem):
                    item.setBrush(QBrush(color))
                elif isinstance(item, QGraphicsItemGroup):
                    for sub_item in item.childItems():
                        if isinstance(sub_item, QGraphicsPathItem):
                            sub_item.setBrush(QBrush(color))
            self.statusBar().showMessage(f"Applied color: {color.name()}")

    def delete_selection(self):
        for item in self.canvas.scene.selectedItems():
            self.canvas.scene.removeItem(item)
        self.statusBar().showMessage("Deleted selected items")

    def load_svg(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open SVG File", "", "SVG Files (*.svg)")
        if not file_path:
            return
        
        self.current_file_path = file_path
        self.canvas.scene.clear()
        self.log_message(f"Loading file: {file_path}")
        
        try:
            # svgelements.SVG.parse can be iterated to get all elements

            svg_data = svg.SVG.parse(file_path)
            
            # Count elements for feedback
            count = 0
            for element in svg_data.elements():
                # self.log_message(f"Found element: {type(element)}")
                # Skip the root SVG element and groups (we handle descendants via iteration often, 
                # but svg_data.elements() yields a flattened list of shapes usually)
                if isinstance(element, (svg.SVG, svg.Group)):
                    continue

                
                try:
                    item = self.create_graphics_item(element)
                    if item:
                        self.canvas.scene.addItem(item)
                        count += 1
                except Exception as ex:
                    self.log_message(f"Failed to create item for {type(element)}: {ex}")
            
            # Adjust view to show all items
            if self.canvas.scene.items():
                rect = self.canvas.scene.itemsBoundingRect()
                self.canvas.setSceneRect(rect.adjusted(-100, -100, 100, 100))
                self.canvas.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatio)
                self.statusBar().showMessage(f"Loaded: {os.path.basename(file_path)} ({count} elements)")
                self.log_message(f"Successfully loaded {count} items.")
            else:
                self.statusBar().showMessage(f"Loaded: {os.path.basename(file_path)} (No renderable elements found)")
                self.log_message("Warning: No renderable items found in SVG.")
                
        except Exception as e:
            self.statusBar().showMessage(f"Error loading SVG: {str(e)}")
            self.log_message(f"Critical Error: {str(e)}")
            import traceback
            self.log_message(traceback.format_exc())

    def create_graphics_item(self, element):
        # Handle Images
        if isinstance(element, svg.SVGImage):
            self.log_message(f"Skipping Image element (support not implemented): {element}")
            return None

        # Convert everything else to a path if possible
        # Check invisibility
        if hasattr(element, 'visibility') and element.visibility == 'hidden':
            return None
            
        try:
            # First try get the path directly (most robust in svgelements for shapes)
            path_data = svg.Path(element)
            
            # Apply transform to the path explicitly if svgelements didn't
            # svgelements.Path(element) usually copies the geometry. 
            # We need to make sure we honor the transform.
            # IN svgelements, path_data usually has the transform applied if created from Shape.
            # But let's check reify().
            path_data.reify() 
            
        except Exception:
            self.log_message(f"Could not convert {type(element)} to Path.")
            return None

        if not path_data or len(path_data) == 0:
            return None

        q_path = QPainterPath()
        try:
            for cmd in path_data:
                if isinstance(cmd, svg.Move):
                    q_path.moveTo(cmd.end.x, cmd.end.y)
                elif isinstance(cmd, svg.Line):
                    q_path.lineTo(cmd.end.x, cmd.end.y)
                elif isinstance(cmd, svg.QuadraticBezier):
                    q_path.quadTo(cmd.control.x, cmd.control.y, cmd.end.x, cmd.end.y)
                elif isinstance(cmd, svg.CubicBezier):
                    q_path.cubicTo(cmd.control1.x, cmd.control1.y, cmd.control2.x, cmd.control2.y, cmd.end.x, cmd.end.y)
                elif isinstance(cmd, svg.Close):
                    q_path.closeSubpath()
        except Exception as e:
             self.log_message(f"Path generation error: {e}")
             return None

        item = QGraphicsPathItem(q_path)
        
        item.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )
        
        # Styles
        # svgelements handles color parsing well
        try:
            fill = element.fill
            if fill is not None and fill != 'none':
                 # fill usually is a Color object
                 if hasattr(fill, 'red'):
                     c = QColor(fill.red, fill.green, fill.blue, int(fill.alpha))
                     item.setBrush(QBrush(c))
                 else:
                     # Fallback
                     item.setBrush(QBrush(QColor(str(fill))))
            else:
                item.setBrush(QBrush(Qt.BrushStyle.NoBrush))
        except Exception:
            item.setBrush(QBrush(Qt.BrushStyle.NoBrush))

        try:
            stroke = element.stroke
            if stroke is not None and stroke != 'none':
                if hasattr(stroke, 'red'):
                     c = QColor(stroke.red, stroke.green, stroke.blue, int(stroke.alpha))
                     pen = QPen(c)
                else:
                     pen = QPen(QColor(str(stroke)))
                
                # width
                sw = element.stroke_width
                if sw is not None:
                    pen.setWidthF(float(sw))
                item.setPen(pen)
            else:
                item.setPen(QPen(Qt.PenStyle.NoPen))
        except Exception:
            item.setPen(QPen(Qt.PenStyle.NoPen))

        return item



    def group_selection(self):
        items = self.canvas.scene.selectedItems()
        if len(items) < 2:
            return
        
        group = QGraphicsItemGroup()
        self.canvas.scene.addItem(group)
        for item in items:
            group.addToGroup(item)
        
        group.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        )
        self.statusBar().showMessage("Grouped selected items")

    def ungroup_selection(self):
        items = self.canvas.scene.selectedItems()
        for item in items:
            if isinstance(item, QGraphicsItemGroup):
                self.canvas.scene.destroyItemGroup(item)
        self.statusBar().showMessage("Ungrouped items")

    def export_selected(self):
        items = self.canvas.scene.selectedItems()
        if not items:
            self.statusBar().showMessage("Nothing selected to export")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Export Selected to SVG", "export.svg", "SVG Files (*.svg)")
        if not file_path:
            return

        try:
            svg_content = ['<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 1000 1000">']
            for item in items:
                svg_content.append(self.item_to_svg_string(item))
            svg_content.append('</svg>')
            
            with open(file_path, 'w') as f:
                f.write('\n'.join(svg_content))
            self.statusBar().showMessage(f"Exported to {file_path}")
        except Exception as e:
            self.statusBar().showMessage(f"Export error: {str(e)}")

    def item_to_svg_string(self, item):
        if isinstance(item, QGraphicsItemGroup):
            sub_items = item.childItems()
            group_str = '<g>'
            for sub in sub_items:
                group_str += self.item_to_svg_string(sub)
            group_str += '</g>'
            return group_str
        
        if isinstance(item, QGraphicsPathItem):
            path = item.path()
            d_parts = []
            
            # Combine scene transform and item transform
            transform = item.sceneTransform()
            
            for i in range(path.elementCount()):
                elem = path.elementAt(i)
                p = transform.map(QPointF(elem.x, elem.y))
                
                if elem.isMoveTo():
                    d_parts.append(f"M {p.x():.2f} {p.y():.2f}")
                elif elem.isLineTo():
                    d_parts.append(f"L {p.x():.2f} {p.y():.2f}")
                elif elem.isCurveTo():
                    # Handle Cubic Bezier
                    cp1 = p
                    elem2 = path.elementAt(i+1)
                    cp2 = transform.map(QPointF(elem2.x, elem2.y))
                    elem3 = path.elementAt(i+2)
                    end = transform.map(QPointF(elem3.x, elem3.y))
                    d_parts.append(f"C {cp1.x():.2f} {cp1.y():.2f}, {cp2.x():.2f} {cp2.y():.2f}, {end.x():.2f} {end.y():.2f}")
            
            d_str = ' '.join(d_parts)
            
            # Extract styles
            brush = item.brush()
            fill = brush.color().name() if brush.style() != Qt.BrushStyle.NoBrush else "none"
            opacity = brush.color().alpha() / 255.0
            
            pen = item.pen()
            stroke = pen.color().name() if pen.style() != Qt.PenStyle.NoPen else "none"
            stroke_width = pen.widthF()
            
            return f'<path d="{d_str}" fill="{fill}" fill-opacity="{opacity:.2f}" stroke="{stroke}" stroke-width="{stroke_width:.2f}" />'
        
        return ""

    def save_svg(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save All as SVG", "drawing.svg", "SVG Files (*.svg)")
        if not file_path:
            return

        try:
            # Calculate total bounding rect for viewBox
            rect = self.canvas.scene.itemsBoundingRect()
            viewbox = f"{rect.x()} {rect.y()} {rect.width()} {rect.height()}"
            
            svg_content = [f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="{viewbox}">']
            # Get items in reverse order to preserve Z-stacking (Qt scene items() is top-down)
            for item in reversed(self.canvas.scene.items()):
                if not item.parentItem():
                    svg_content.append(self.item_to_svg_string(item))
            svg_content.append('</svg>')
            
            with open(file_path, 'w') as f:
                f.write('\n'.join(svg_content))
            self.statusBar().showMessage(f"Saved all to {file_path}")
        except Exception as e:
            self.statusBar().showMessage(f"Save error: {str(e)}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_Backspace:
            for item in self.canvas.scene.selectedItems():
                self.canvas.scene.removeItem(item)
            self.statusBar().showMessage("Deleted selected items")
        elif event.matches(QKeySequence.StandardKey.SelectAll):
            for item in self.canvas.scene.items():
                item.setSelected(True)
        else:
            super().keyPressEvent(event)


    def export_split_all(self):
        """Export all top-level items as separate SVG files: OriginalName_1.svg, etc."""
        items = [item for item in self.canvas.scene.items(Qt.SortOrder.AscendingOrder) if not item.parentItem()]
        if not items:
            self.statusBar().showMessage("No items to export")
            return

        if not self.current_file_path:
            self.statusBar().showMessage("Save or Open a file first to establish naming base.")
            # Fallback to asking user
            base_path, _ = QFileDialog.getSaveFileName(self, "Select Base Filename", "split_export", "SVG Files (*.svg)")
            if not base_path:
                return
            self.current_file_path = base_path

        base_name = os.path.splitext(os.path.basename(self.current_file_path))[0]
        directory = os.path.dirname(self.current_file_path)
        
        # Ask for confirmation or directory? Let's just do it in the same dir for now to be fast
        # Or better, create a subdir to avoid clutter
        export_dir = os.path.join(directory, f"{base_name}_parts")
        os.makedirs(export_dir, exist_ok=True)
        
        msg = f"Exporting {len(items)} items to {export_dir}..."
        self.statusBar().showMessage(msg)
        self.log_message(msg)
        
        try:
            for i, item in enumerate(items, 1):
                filename = f"{base_name}_{i}.svg"
                file_path = os.path.join(export_dir, filename)
                
                # Get item bounds for viewbox
                rect = item.sceneBoundingRect()
                # Create SVG with tight viewbox around item
                
                viewbox = f"{rect.x()} {rect.y()} {rect.width()} {rect.height()}"
                svg_content = [f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="{viewbox}">']
                svg_content.append(self.item_to_svg_string(item))
                svg_content.append('</svg>')
                
                with open(file_path, 'w') as f:
                    f.write('\n'.join(svg_content))
            
            success_msg = f"Successfully exported {len(items)} files to {export_dir}"
            self.statusBar().showMessage(success_msg)
            self.log_message(success_msg)
            
            # Open the folder for user convenience
            try:
                from PyQt6.QtGui import QDesktopServices
                from PyQt6.QtCore import QUrl
                QDesktopServices.openUrl(QUrl.fromLocalFile(export_dir))
            except:
                pass
            
        except Exception as e:
            self.log_message(f"Split export failed: {e}")

    def zoom_in(self):
        self.canvas.scale(1.2, 1.2)

    def zoom_out(self):
        self.canvas.scale(1/1.2, 1/1.2)

    def reset_zoom(self):
        if self.canvas.scene.items():
            self.canvas.fitInView(self.canvas.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
        else:
            self.canvas.resetTransform()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


