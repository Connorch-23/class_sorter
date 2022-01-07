package org.class_sorter.view;

import javafx.event.EventHandler;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.scene.text.Font;
import org.class_sorter.controller.Controller;
import org.class_sorter.model.Camper;
import org.class_sorter.model.Model;
import org.class_sorter.model.ModelObserver;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

public class PromptView extends Node implements FXComponent, ModelObserver {
    private final Controller controller;

    public PromptView(Controller controller) {
        if (controller == null) {
            throw new IllegalArgumentException();
        }
        this.controller = controller;
    }

    @Override
    public void update(Model model) {
        render();
    }

    @Override
    public Parent render() {

        StackPane pane = new StackPane();

        VBox vbox = new VBox();
        pane.getChildren().add(vbox);
        vbox.setPrefSize(500,300);
        vbox.setAlignment(Pos.CENTER);

        Label instructions = new Label("Give your file of sorted campers a name!");
        instructions.getStyleClass().add("label");
        vbox.getChildren().add(instructions);
        instructions.setFont(new Font("Georgia",15));
        instructions.setPadding(new Insets(5));

        final TextField fileName = new TextField();
        fileName.setPromptText("Name for new file");
        fileName.setFont(new Font("Georgia",15));
        fileName.setPadding(new Insets(5));
        fileName.setAlignment(Pos.BASELINE_CENTER);
        vbox.getChildren().add(fileName);

        Button button = new Button("Click to sort into Classes!");
        button.setFont(new Font("Georgia",15));
        button.setPadding(new Insets(5));
        button.getStyleClass().add("label");
        vbox.getChildren().add(button);


        if (controller.getIsSorted()) {

            StackPane completedFrame = new StackPane();


            VBox completedVbox = new VBox();
            completedVbox.setAlignment(Pos.CENTER);
            completedVbox.setPadding(new Insets(20,20,20,20));

            Label nameOfFile = new Label("Your new file is named: " + controller.getFileName());
            nameOfFile.setFont(new Font("Georgia",15));
            nameOfFile.setPadding(new Insets(5));

            Label goFindIt = new Label("You can find it by looking up " + controller.getFileName() + " on your machine!");
            goFindIt.setFont(new Font("Georgia",15));
            goFindIt.setPadding(new Insets(5));


            Label iDidThis = new Label("This program was made by Connor Hitchings :)");
            iDidThis.setFont(new Font("Georgia",15));
            iDidThis.setPadding(new Insets(5));


            completedFrame.getChildren().add(completedVbox);
            completedVbox.getChildren().add(nameOfFile);
            completedVbox.getChildren().add(goFindIt);
            completedVbox.getChildren().add(iDidThis);
            completedFrame.autosize();


            return completedFrame;
        }


        button.setOnMouseClicked(
                new EventHandler<MouseEvent>() {
                    @Override
                    public void handle(MouseEvent mouseEvent) {
                            FileWriter writer = null;
                            try {
                                String name;
                                name = fileName.getText();
                                controller.setFileName(name);
                                writer = new FileWriter(name);
                                List<Camper> campersList;
                                campersList = controller.getSortedCampers();
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
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                    }
                }
        );

        return pane;
    }

}
