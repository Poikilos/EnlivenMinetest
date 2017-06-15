#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QLabel>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    double scaleFactor;
    void setImage(const QImage &newImage, int imageIndex);  // QLabel* imageLabel);
    void createActions();
    bool loadImage(QString &fileName, int imageIndex);  // QLabel* imageLabel);
    Ui::MainWindow *ui;
    QImage upperImage;
    QImage lowerImage;

public slots:
    void showGraphics();
    void launchGame();
};

#endif // MAINWINDOW_H
