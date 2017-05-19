#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QFileInfo>
#include <QDir>
//#include <QPixmap>
//#include <QGraphicsPixmapItem>
#include <QDebug>
//#include <QGuiApplication>
#include <QScreen>
#include <QImage>
#include <QImageReader>
#include <QMessageBox>
#include <QTimer>
#include <QProcess>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->scaleFactor = 1.0;

    ui->upperImageLabel->setBackgroundRole(QPalette::Base);
    ui->upperImageLabel->setSizePolicy(QSizePolicy::Ignored, QSizePolicy::Ignored);
    ui->upperImageLabel->setScaledContents(true);
    ui->lowerImageLabel->setBackgroundRole(QPalette::Base);
    ui->lowerImageLabel->setSizePolicy(QSizePolicy::Ignored, QSizePolicy::Ignored);
    ui->lowerImageLabel->setScaledContents(true);
    //setCentralWidget(verticalLayout);
    createActions();
    //resize(QGuiApplication::primaryScreen()->availableSize() * 3 / 5);
    //resize(ui->lowerImageLabel->width());
    QFileInfo selfFI(QCoreApplication::applicationFilePath());
    QDir selfDir=selfFI.absoluteDir();
    QDir binDir(selfDir.absoluteFilePath("bin"));
    QString minetestExePath = binDir.absoluteFilePath("minetest.exe");
    bool success_enable = false;
    if (!QFileInfo(minetestExePath).exists()) {
        QString try_path="C:\\games\\ENLIVEN\\bin\\minetest.exe";
        if (QFileInfo(try_path).exists()) {
            minetestExePath = try_path;
        }
    }
    if (!QFileInfo(minetestExePath).exists()) {
        QString try_path="C:\\Program Files (x86)\\ENLIVEN\\bin\\minetest.exe";
        if (QFileInfo(try_path).exists()) {
            minetestExePath = try_path;
        }
    }
    if (QFileInfo(minetestExePath).exists()) {
        QProcess* newProcess = new QProcess();
        QDir workingDir = QFileInfo(minetestExePath).absoluteDir();
        // Will not launch the application
        newProcess->setWorkingDirectory(workingDir.absolutePath());
        newProcess->start(minetestExePath);
        success_enable = true;
        qDebug() << "launched " << minetestExePath;
    }
    if (success_enable) QTimer::singleShot(1000, this, &QApplication::closeAllWindows); // Qt 5
    //QApplication::closeAllWindows();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::setImage(const QImage &newImage, int imageIndex) //QLabel* imageLabel)
{
    if (imageIndex==0) {
        upperImage = newImage;
        ui->upperImageLabel->setPixmap(QPixmap::fromImage(upperImage));
    }
    else {
        lowerImage = newImage;
        ui->lowerImageLabel->setPixmap(QPixmap::fromImage(lowerImage));
    }
    scaleFactor = 1.0;

    //scrollArea->setVisible(true);
    //printAct->setEnabled(true);
    //fitToWindowAct->setEnabled(true);
    //updateActions();

    //if (!fitToWindowAct->isChecked())
    //    imageLabel->adjustSize();
}

void MainWindow::createActions()
{
    //see http://doc.qt.io/qt-5/qtwidgets-widgets-imageviewer-example.html
    QFileInfo selfFI(QCoreApplication::applicationFilePath());
    QDir selfDir=selfFI.absoluteDir();
    QDir gamesDir(selfDir.absoluteFilePath("games"));
    QDir enlivenDir(gamesDir.absoluteFilePath("ENLIVEN"));
    QDir menuImagesDir(enlivenDir.absoluteFilePath("menu"));
    QString upperImagePath=menuImagesDir.absoluteFilePath("header.png");
    QString lowerImagePath=menuImagesDir.absoluteFilePath("icon.png");
    if (QFileInfo(upperImagePath).exists()) {
        loadImage(upperImagePath, 0);// ui->upperImageLabel);
        //below is NONWORKING from http://stackoverflow.com/questions/1357960/qt-jpg-image-display
        //QGraphicsPixmapItem upperItem(QPixmap(upperImagePath));
        //QGraphicsScene upperScene;
        //ui->upperGraphicsView->setScene(&upperScene);
        //upperScene.addItem(&upperItem);
    }
    else qDebug() << tr("missing ") << upperImagePath;
    if (QFileInfo(lowerImagePath).exists()) {
        loadImage(lowerImagePath, 1);//ui->lowerImageLabel);
        //below is NONWORKING from http://stackoverflow.com/questions/1357960/qt-jpg-image-display
        //QGraphicsPixmapItem lowerItem(QPixmap(lowerImagePath));
        //QGraphicsScene lowerScene;
        //ui->upperGraphicsView->setScene(&lowerScene);
        //lowerScene.addItem(&lowerItem);
    }
    else qDebug() << tr("missing ") << lowerImagePath;
}

bool MainWindow::loadImage(QString &fileName, int imageIndex) //, QLabel* imageLabel)
{
    QImageReader reader(fileName);
    reader.setAutoTransform(true);
    const QImage newImage = reader.read();
    if (newImage.isNull()) {
        QMessageBox::information(this, QGuiApplication::applicationDisplayName(),
                                 tr("Cannot load %1: %2")
                                 .arg(QDir::toNativeSeparators(fileName), reader.errorString()));
        return false;
    }
    setImage(newImage, imageIndex);// imageLabel);
    //ui->scrollArea->setVisible(true);
    //printAct->setEnabled(true);
    //fitToWindowAct->setEnabled(true);
    //updateActions();

    //if (!fitToWindowAct->isChecked())
        //imageLabel->adjustSize();
}

void MainWindow::showGraphics()
{

}

void MainWindow::launchGame()
{

}
