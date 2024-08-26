// views/CalibrateModal.qml
import QtQuick 2.15
import QtQuick.Controls 2.15

Dialog {
    id: calibrateDialog
    modal: true
    dim: true
    focus: true
    visible: true
    height: 200
    width: 300

    Column {
        spacing: 10
        padding: 20

        Text {
            text: "Calibrating..."
            font.pointSize: 20
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }

        ProgressBar {
            id: progressBar
            width: 200
            value: 0.0
            indeterminate: true  // Progress bar will be indeterminate
        }

        // A spacer to add some space below the progress bar
        Rectangle {
            height: 10
            color: "transparent"
        }
    }

    // Function to update the progress (if you want to have a determinate progress bar)
    function updateProgress(value) {
        progressBar.value = value
    }

    // Prevent closing the dialog with Esc or clicking outside
    onAccepted: {
        calibrateDialog.visible = false
    }
    onRejected: {
        calibrateDialog.visible = false
    }

    Component.onCompleted: {
        calibrateDialog.visible = true
    }
}
