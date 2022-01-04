package org.class_sorter.view;

import javafx.event.EventHandler;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Parent;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;
import org.class_sorter.controller.Controller;
import org.class_sorter.model.Camper;
import org.class_sorter.model.Model;
import org.class_sorter.model.ModelObserver;

import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

public class PromptView implements FXComponent, ModelObserver {
    private Controller controller;
    private Model model;


    public PromptView(Controller controller, Model model) {
        if (controller == null) {
            throw new IllegalArgumentException();
        }
        this.controller = controller;
        this.model = model;
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
        vbox.setPrefSize(400,200);
        vbox.setAlignment(Pos.CENTER);

        final TextField fileName = new TextField();
        fileName.setPromptText("Name for new file");
        vbox.getChildren().add(fileName);

        Button button = new Button("Sort into Classes!");
        button.getStyleClass().add("label");
        vbox.getChildren().add(button);
        button.setOnMouseClicked(
                new EventHandler<MouseEvent>() {
                    @Override
                    public void handle(MouseEvent mouseEvent) {
                        List<Camper> campersList;
                        campersList = controller.getSortedCampers();
                        FileWriter writer = null;
                        try {
                            writer = new FileWriter("test.csv");
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                        try {
                            assert writer != null;
                            writer.append("Last Name");
                            writer.append(",");
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
