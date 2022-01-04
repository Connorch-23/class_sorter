package org.class_sorter.view;

import javafx.geometry.Insets;
import javafx.scene.Parent;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;
import org.class_sorter.controller.Controller;
import org.class_sorter.model.Model;
import org.class_sorter.model.ModelObserver;

import javax.swing.*;

public class View implements FXComponent, ModelObserver {
    private Controller controller;
    private Model model;

    public View(Controller controller, Model model) {
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


        pane.setPadding(new Insets(100, 200, 100, 200));

        return pane;
    }


}
