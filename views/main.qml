import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "Shot Timer"

    StackView {
        id: stackView
        anchors.fill: parent

        initialItem: mainScreen
    }

    Component {
        id: mainScreen
        Row {
            anchors.fill: parent

            // Left Panel: Drill List
            Rectangle {
                width: parent.width * 0.4
                height: parent.height
                color: "#1E1E1E" // Dark gray
                radius: 10

                ListView {
                    width: parent.width
                    height: parent.height
                    model: drillsModel
                    clip: true  // Ensures items do not overflow

                    // Property to store the selected index
                    property int selectedIndex: vm.selectedIndex

                    delegate: Item {
                        width: parent.width
                        height: 60

                        // Highlight the selected item
                        Rectangle {
                            anchors.fill: parent
                            color: vm.selectedIndex == index ? "lightblue" : "transparent"

                            MouseArea {
                                anchors.fill: parent
                                onClicked: {
                                    vm.selectedIndex = index
                                }
                            }

                            Column {
                                anchors.fill: parent
                                spacing: 5

                                Text {
                                    text: name
                                    font.bold: true
                                    font.pointSize: 18
                                    color: "white"
                                }

                                Text {
                                    text: description
                                    font.pointSize: 14
                                    color: "white"
                                }
                            }
                        }
                    }
                }
            }

            // Right Panel: Drill Details or Timer
            Rectangle {
                color: "#2C2C2C" // Slightly lighter gray for contrast
                width: parent.width * 0.6
                height: parent.height

                Column {
                    anchors.centerIn: parent
                    spacing: 20

                    Button {
                        text: "Start Timer"
                        onClicked: {
                            // Navigate to the Timer screen
                            if(vm.selectedIndex === -1) {
                                console.log("Please select a drill to start the timer")
                            } else {
                                timerScreenViewModel.selectedIndex = vm.selectedIndex
                                stackView.push(Qt.resolvedUrl("timer_screen.qml"))
                            }
                        }
                    }

                    Button {
                        text: "View History"
                        onClicked: {
                            // Navigate to view history
                            if(vm.selectedIndex === -1) {
                                console.log("Please select a drill to start the timer")
                            } else {
                                viewHistoryScreenViewModel.selectedIndex = vm.selectedIndex
                                stackView.push(Qt.resolvedUrl("view_history_screen.qml"))
                            }
                        }
                    }

                    Button {
                        text: "View Analytics"
                        onClicked: {
                            // Navigate to view analytics
                            if(vm.selectedIndex === -1) {
                                console.log("Please select a drill to start the timer")
                            } else {
                                viewAnalyticsScreenViewModel.selectedIndex = vm.selectedIndex
                                stackView.push(Qt.resolvedUrl("view_analytics_screen.qml"))
                            }
                        }
                    }

                    Button {
                        text: "Calibrate"
                        onClicked: {
                            // Load and show the calibration modal
                            calibrator.calibrate()
                        }
                    }

                    Button {
                        text: "Test Calibration"
                        onClicked: {
                            // Load and show the calibration modal
                            calibrator.test()
                        }
                    }

                    Button {
                        text: "Dump Data"
                        onClicked: {
                            // Logic to dump data
                        }
                    }

                    Button {
                        text: "Delete All Data"
                        onClicked: {
                            // Logic to delete all data
                        }
                    }
                }
            }
        }
    }
}
