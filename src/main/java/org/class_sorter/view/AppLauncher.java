package org.class_sorter.view;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;
import org.class_sorter.CamperLibrary;
import org.class_sorter.model.Class_;

import java.util.List;

public class AppLauncher extends Application {
    @Override
    public void start(Stage stage) {
        List<Class_> list = CamperLibrary.getClasses();
        
    }
}
