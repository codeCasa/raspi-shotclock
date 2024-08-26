import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    width: 800
    height: 800
    color: "#2C2C2C" // Dark gray background

    Row {
        anchors.fill: parent
        spacing: 10 // Add spacing between the panels

        // Left Panel: Drill Meta Information
        Rectangle {
            width: parent.width * 0.4
            height: parent.height
            color: "#1E1E1E" // Even darker gray for contrast
            radius: 10

            Column {
                spacing: 10
                anchors.centerIn: parent

                Text {
                    text: "Drill Name: " + timerScreenViewModel.drillName
                    font.pointSize: 20
                    color: "white"
                    font.bold: true
                    wrapMode: Text.Wrap
                }

                Text {
                    text: "Description: " + timerScreenViewModel.drillDescription
                    font.pointSize: 16
                    color: "white"
                    wrapMode: Text.Wrap
                }

                Text {
                    text: "Number of Shots: " + timerScreenViewModel.numberOfShots
                    font.pointSize: 16
                    color: "white"
                    wrapMode: Text.Wrap
                }

                Button {
                    text: "Go Back"
                    onClicked:  {
                        stackView.pop()
                    }
                }
            }
        }

        // Right Panel: Timer and Control UI
        Rectangle {
            width: parent.width * 0.6
            height: parent.height
            color: "#2C2C2C" // Dark gray background for consistency
            radius: 10

            Column {
                spacing: 20
                anchors.fill: parent // Fill the available space in the parent
                anchors.margins: 10

                // Timer display
                Text {
                    text: timerScreenViewModel.timerState === 4 ? "Countdown: " + timerScreenViewModel.countdownTime : "Elapsed Time: " + timerScreenViewModel.elapsedTime
                    font.pointSize: 24
                    color: "white"
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                // Buttons for timer control
                Row {
                    spacing: 10
                    anchors.horizontalCenter: parent.horizontalCenter

                    Button {
                        function getStartBtnText() {
                            if (timerScreenViewModel.timerState == 0 || timerScreenViewModel.timerState == 1) {
                                return "Pause"
                            } else if (timerScreenViewModel.timerState == 2) {
                                return "Resume"
                            } else {
                                return "Start"
                            }
                        }
                        text: getStartBtnText()
                        onClicked: {
                            if (timerScreenViewModel.timerState == 0 || timerScreenViewModel.timerState == 1) {
                                timerScreenViewModel.pauseTimer()
                            } else if (timerScreenViewModel.timerState == 2) {
                                timerScreenViewModel.resumeTimer()
                            } else if (timerScreenViewModel.timerState == 4) {
                                timerScreenViewModel.stopTimer()
                                timerScreenViewModel._startTimerNow()
                            } else {
                                timerScreenViewModel.startTimer()
                            }
                        }
                    }

                    Button {
                        text: "Stop Timer"
                        onClicked: timerScreenViewModel.stopTimer()
                    }
                }

                Row {
                    spacing: 10
                    anchors.horizontalCenter: parent.horizontalCenter

                    Button {
                        id: addShotButton
                        text: "+1 Shot Fired"
                        enabled: timerScreenViewModel.timerState == 1 || timerScreenViewModel.timerState == 0
                        onClicked: timerScreenViewModel.addShotFired()
                    }

                    Text {
                        text: "Shots Fired: " + timerScreenViewModel.shotsFired
                        font.pointSize: 16
                        color: "white"
                        wrapMode: Text.Wrap
                        anchors.verticalCenter: addShotButton.verticalCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }

                // Split times and result entry
                Row {
                        spacing: 10
                        // anchors.horizontalCenter: parent.horizontalCenter
                        height: 200
                        width: parent.width
                        
                        // Split times list
                        ListView {
                            width: parent.width * 0.4 // Adjust width to prevent overlap
                            height: 200
                            model: timerScreenViewModel.splits
                            visible: timerScreenViewModel.wasStarted
                            clip: true
                            delegate: Text {
                                text: "Shot #"+(index +1)+": "+ modelData
                                font.pointSize: 18
                                color: "white"
                            }
                        }

                        // Section to enter score and notes
                        Rectangle {
                            visible: timerScreenViewModel.timerState === 3 && timerScreenViewModel.wasStarted  // Only visible when timer is stopped and has been started
                            color: "#4F4F4F" // Light gray
                            radius: 10
                            width: parent.width * 0.6 // Adjust width to fit the remaining space
                            anchors.right: parent.right

                            Column {
                                spacing: 10
                                anchors.margins: 10
                                anchors.fill: parent

                                TextField {
                                    id: scoreField
                                    placeholderText: "Enter Score (if applicable)"
                                    text: ""
                                    font.pointSize: 18
                                    placeholderTextColor: "white"
                                    color: "#2C2C2C"
                                    width: parent.width
                                }

                                TextField {
                                    id: notesField
                                    placeholderText: "Enter Notes"
                                    text: ""
                                    font.pointSize: 18
                                    placeholderTextColor: "white"
                                    color: "#2C2C2C"
                                    width: parent.width
                                }

                                Button {
                                    text: "Save Results"
                                    onClicked: {
                                        let score = parseFloat(scoreField.text) || null
                                        let notes = notesField.text
                                        timerScreenViewModel.saveResults(score, notes)
                                    }
                                    anchors.horizontalCenter: parent.horizontalCenter
                                }
                            }
                        }
                    
                }
            }
        }
    }
}
