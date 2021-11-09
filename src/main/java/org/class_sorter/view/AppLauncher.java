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
        List<Camper> campersList = model.getCampers();
        campersList = controller.getSortedCampers();
        FileWriter writer = new FileWriter("test.csv");
        writer.append("Last Name");
        writer.append(",");
        writer.append("First Name");
        writer.append(",");
        writer.append("Cabin");
        writer.append(",");
        writer.append("Class A");
        writer.append(",");
        writer.append("Class B");
        writer.append(",");
        writer.append("Class C");
        writer.append(",");
        writer.append("Class D");
        writer.append("\n");


        for (Camper c : campersList) {
            writer.append(c.getLastName());
            writer.append(",");
            writer.append(c.getFirstName());
            writer.append(",");
            writer.append(c.getCabin());
            writer.append(",");
            String className = "ERROR1";

            if (c.getClassA() != null) {
                className = c.getClassA().getName();
            }
            writer.append(className);
            writer.append(",");
            className = "ERROR1";

            if (c.getClassB() != null) {
                className = c.getClassB().getName();
            }
            writer.append(className);
            writer.append(",");
            className = "ERROR1";

            if (c.getClassC() != null) {
                className = c.getClassC().getName();
            }
            writer.append(className);
            writer.append(",");
            className = "ERROR1";

            if (c.getClassD() != null) {
                className = c.getClassD().getName();
            }
            writer.append(className);
            writer.append("\n");

        }
        writer.flush();
        writer.close();
        Scene scene = new Scene(view.render());
        stage.setScene(scene);
        model.addObserver(
                (Model m) -> {
                    scene.setRoot(view.render());
                    stage.sizeToScene();
                });
        stage.setTitle(selectedFile1.getName());
        stage.show();
    }
}
