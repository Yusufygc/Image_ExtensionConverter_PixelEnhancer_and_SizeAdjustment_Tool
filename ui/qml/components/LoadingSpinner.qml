import QtQuick
import ".."

Item {
    id: root
    property int size: 20
    property color color: FluentTheme.accent
    property bool running: true

    width: size
    height: size

    Canvas {
        id: canvas
        anchors.fill: parent
        antialiasing: true

        onPaint: {
            var ctx = getContext("2d");
            ctx.reset();
            var centerX = width / 2;
            var centerY = height / 2;
            var radius = (Math.min(width, height) - 4) / 2;

            // Background subtle track
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
            ctx.lineWidth = 2.5;
            ctx.strokeStyle = Qt.rgba(root.color.r, root.color.g, root.color.b, 0.2);
            ctx.stroke();

            // Active spinning arc
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, Math.PI * 0.8);
            ctx.lineWidth = 2.5;
            ctx.strokeStyle = root.color;
            ctx.lineCap = "round";
            ctx.stroke();
        }
    }

    RotationAnimation {
        target: canvas
        from: 0
        to: 360
        duration: 800
        loops: Animation.Infinite
        running: root.running && root.visible
    }
}
