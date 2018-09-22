import math
import sys

from PyQt5 import QtGui, QtWidgets

from code_wheel.resources import resources_rc


def wheel_radius(pixmap_item):
    """
    Determine the radius of the given wheel part.

    :param pixmap_item: The wheel part.
    :type pixmap_item:  QtWidgets.QPixmapGraphicsItem

    :returns: The radius of the given wheel.
    :rtype:   float
    """
    return pixmap_item.boundingRect().width() / 2


def rotation(position, wheel):
    """
    Calculate the rotation angle (in degrees) of the given position on the given wheel.

    :param position: The position os the mouse.
    :type position:  QtGui.QPosition

    :param wheel: The wheel part.
    :type wheel:  QtWidgets.QPixmapGraphicsItem

    :returns: The rotation angle of the mouse in degrees.
    :rtype:   float
    """
    center = wheel.boundingRect().center()

    position = position - center

    rotation = math.atan2(position.y(), position.x())

    return math.degrees(rotation) + 180


class Scene(QtWidgets.QGraphicsScene):
    """A graphics scene containing the code wheel from bard's tale 4."""

    def __init__(self):
        """Add the parts of the wheel to the scene."""
        super().__init__()
        self.current_wheel = None
        self.pressed = False
        self.click_position = None
        self.starting_rotation = 0

        # Set the background to be a comfortable black.
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor('#252525')))

        # Set up all the wheels and make them rotate around their centers.
        self.bottom_wheel = self.addPixmap(QtGui.QPixmap(':/bottom_wheel.png'))
        self.bottom_wheel.setTransformOriginPoint(wheel_radius(self.bottom_wheel), wheel_radius(self.bottom_wheel))

        self.middle_wheel = self.addPixmap(QtGui.QPixmap(':/middle_wheel.png'))
        self.middle_wheel.setTransformOriginPoint(wheel_radius(self.middle_wheel), wheel_radius(self.middle_wheel))
        self.middle_wheel.moveBy(
            wheel_radius(self.bottom_wheel) - wheel_radius(self.middle_wheel),
            wheel_radius(self.bottom_wheel) - wheel_radius(self.middle_wheel),
        )

        self.top_wheel = self.addPixmap(QtGui.QPixmap(':/top_wheel.png'))
        self.top_wheel.setTransformOriginPoint(wheel_radius(self.top_wheel), wheel_radius(self.top_wheel))
        self.top_wheel.moveBy(
            wheel_radius(self.bottom_wheel) - wheel_radius(self.top_wheel),
            wheel_radius(self.bottom_wheel) - wheel_radius(self.top_wheel),
        )

    def mousePressEvent(self, event):
        """
        Called when the mouse is pressed.

        Determine which part of the wheel was clicked.

        :param event: The mouse press event.
        :type event:  QtWidgets.QGraphicsSceneMouseEvent
        """
        clicked_item = self.itemAt(event.scenePos().x(), event.scenePos().y(), self.views()[0].transform())
        if clicked_item is None:
            return

        self.pressed = True
        self.click_position = event.scenePos()

        self.current_wheel = clicked_item
        self.starting_rotation = self.current_wheel.rotation()

    def mouseReleaseEvent(self, event):
        """
        Called when the mouse is released.

        Reset all of the cached values about what was clicked.

        :param event: The mouse press event.
        :type event:  QtWidgets.QGraphicsSceneMouseEvent
        """
        self.click_position = None
        self.current_wheel = None
        self.original_rotation = None
        self.pressed = False
        self.starting_rotation = 0

    def mouseMoveEvent(self, event):
        """
        Called when the mouse is moved.

        If any part of the wheel was selected and the mouse is still pressed, determine
        how much we need to rotate the selected part.

        :param event: The mouse press event.
        :type event:  QtWidgets.QGraphicsSceneMouseEvent
        """
        if not self.pressed or self.current_wheel is None:
            return

        click_rotation = rotation(self.click_position, self.current_wheel)
        current_rotation = rotation(event.scenePos(), self.current_wheel)

        self.current_wheel.setRotation(self.starting_rotation + (current_rotation - click_rotation))


def main():
    """Run the program."""
    app = QtWidgets.QApplication([])
    app.setApplicationName('Bard\'s Tale IV Code Wheel')
    app.setWindowIcon(QtGui.QIcon(':icon.ico'))

    scene = Scene()

    view = QtWidgets.QGraphicsView(scene)
    view.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
