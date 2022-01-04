package org.class_sorter.view;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import org.class_sorter.CamperLibrary;
import org.class_sorter.controller.Controller;
import org.class_sorter.controller.ControllerImpl;
import org.class_sorter.model.Camper;
import org.class_sorter.model.Class_;
import org.class_sorter.model.Model;
import org.class_sorter.model.ModelImpl;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class AppLauncher extends Application {

    @Override
    public void start(Stage stage) throws IOException {
        FileChooser fileChooser1 = new FileChooser();
        fileChooser1.setTitle("Open Resource File");
        File selectedFile1 = fileChooser1.showOpenDialog(stage);

        FileChooser fileChooser2 = new FileChooser();
        fileChooser2.setTitle("Open Resource File");
        File selectedFile2 = fileChooser2.showOpenDialog(stage);

        Model model = new ModelImpl();

        model.createCampers(selectedFile1);
        model.createClasses(selectedFile2);
        for(Camper camper : model.getCampers()) {
            camper.cleanPrefs(model.getClasses());
        }

        Controller controller = new ControllerImpl(model);

        View view = new View(controller, model);



         //Code for prompt box asking what new campers file should be





        PromptView promptView = new PromptView(controller,model);
        Scene scene = new Scene(promptView.render());
        stage.setScene(scene);
        model.addObserver(
                (Model m) -> {
                    scene.setRoot(promptView.render());
                    stage.sizeToScene();
                });
        stage.setTitle("Class Sorter");
        stage.show();

    }
}
