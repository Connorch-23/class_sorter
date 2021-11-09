package org.class_sorter;

import static org.junit.Assert.assertTrue;

import org.class_sorter.model.*;
import org.junit.Test;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Unit test for simple App.
 */
public class AppTest {
    @Test
    public void shouldAnswerWithTrue() {
        assertTrue(true);
    }

    @Test
    public void instantiateTest() {

        List<Class_> classes = new ArrayList<>();
        Class_ paintball = new ClassImpl("Paintball", 10, true);
        Class_ horses = new ClassImpl("Horse Back Riding", 15, false);
        Class_ kayaking = new ClassImpl("Kayaking", 15, false);
        Class_ drama = new ClassImpl("Drama", 12, false);
        Class_ rifles = new ClassImpl("Rifles", 12, true);
        Class_ shotguns = new ClassImpl("FiveStand", 10, true);
        Class_ photography = new ClassImpl("Photography", 10, false);
        Class_ climbing = new ClassImpl("Climbing", 15, false);
        Class_ fishing = new ClassImpl("Fishing", 5, false);
        Class_ archery = new ClassImpl("Archery", 9, false);
        Class_ sports = new ClassImpl("Sports", 13, false);

        classes.add(paintball);
        classes.add(horses);
        classes.add(kayaking);
        classes.add(drama);
        classes.add(rifles);
        classes.add(shotguns);
        classes.add(photography);
        classes.add(climbing);
        classes.add(fishing);
        classes.add(archery);
        classes.add(sports);

        List<String> pref1 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            int n = (int) (Math.random() * (10));
            if (!pref1.contains(classes.get(n).getName())) {
                pref1.add(classes.get(n).getName());
            } else {
                i--;
            }
        }

        List<String> pref2 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            int n = (int) (Math.random() * (10));
            if (!pref2.contains(classes.get(n).getName())) {
                pref2.add(classes.get(n).getName());
            } else {
                i--;
            }
        }
        List<String> pref3 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            int n = (int) (Math.random() * (10));
            if (!pref3.contains(classes.get(n).getName())) {
                pref3.add(classes.get(n).getName());
            } else {
                i--;
            }
        }
        List<String> pref4 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            int n = (int) (Math.random() * (10));
            if (!pref4.contains(classes.get(n).getName())) {
                pref4.add(classes.get(n).getName());
            } else {
                i--;
            }
        }
        List<String> pref5 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            int n = (int) (Math.random() * (10));
            if (!pref5.contains(classes.get(n).getName())) {
                pref5.add(classes.get(n).getName());
            } else {
                i--;
            }
        }
        List<String> pref6 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            int n = (int) (Math.random() * (10));
            if (!pref6.contains(classes.get(n).getName())) {
                pref6.add(classes.get(n).getName());
            } else {
                i--;
            }
        }
        List<String> pref7 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            int n = (int) (Math.random() * (10));
            if (!pref7.contains(classes.get(n).getName())) {
                pref7.add(classes.get(n).getName());
            } else {
                i--;
            }
        }
        List<String> pref8 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            int n = (int) (Math.random() * (10));
            if (!pref8.contains(classes.get(n).getName())) {
                pref8.add(classes.get(n).getName());
            } else {
                i--;
            }
        }

        List<List<String>> preferences = new ArrayList<>();
        preferences.add(pref1);
        preferences.add(pref2);
        preferences.add(pref3);
        preferences.add(pref4);
        preferences.add(pref5);
        preferences.add(pref6);
        preferences.add(pref7);
        preferences.add(pref8);


        Camper charlie = new CamperImpl("Charlie", "Hunnam", "EX", "4L", true, pref1);
        Camper Mack = new CamperImpl("Mack", "Johnson", "EX","3L", true, pref3);
        Camper Lizzie = new CamperImpl("Lizzie", "Harrison", "EX","3", false, pref5);
        Camper Ellie = new CamperImpl("Ellie", "Counts","EX", "15A", true, pref7);
        Camper Chase = new CamperImpl("Chase", "Mccrary","EX", "7", false, pref8);
        Camper Nick = new CamperImpl("Nick", "Budd", "EX", "12", true, pref2);
        Camper John = new CamperImpl("John", "Brown", "EX", "12", true, pref3);
        Camper Nathan = new CamperImpl("Nathan", "Peterman", "EX", "12", true, pref4);
        Camper Marissa = new CamperImpl("Marissa", "Forfar", "EX", "10", true, pref7);
        Camper Sherry = new CamperImpl("Mark", "Carr", "EX", "14", true, pref5);
        Camper Carlos = new CamperImpl("Carlos", "Santana", "EX", "9", true, pref3);
        Camper Haley = new CamperImpl("Haley", "Atwell","EX", "10", true, pref1);
        Camper Patrick = new CamperImpl("Patrick", "Mahomes", "EX", "12", true, pref6);


    }

    @Test
    public void csvTest0() throws FileNotFoundException {
        Model model = new ModelImpl();
        model.createCampers(new File("/Users/connorhitchings/Desktop/Campers-test.csv"));
        for (Camper c : model.getCampers()) {
            System.out.println(c.getFirstName() + " " + c.getLastName());
            System.out.println(c.getAgeGroup());
            System.out.println(c.getCabin());
            System.out.println(c.getCanShoot());
            for (String s : c.getPrefs()) {
                System.out.println(s);
            }
        }
    }

    @Test
    public void csvTest1() throws FileNotFoundException {
        Model model = new ModelImpl();
        model.createClasses(new File("/Users/connorhitchings/Desktop/Classes-test.csv"));
        for (Class_ c : model.getClasses()) {
            System.out.println(c.getName());
            System.out.println(c.getCapacity());
            System.out.println(c.getRequiresShootingForm());

        }
    }

    @Test
    public void sortTest0() throws FileNotFoundException {
        Model model = new ModelImpl();
        model.createCampers(new File("/Users/connorhitchings/Desktop/Campers-test.csv"));
        model.createClasses(new File("/Users/connorhitchings/Desktop/Classes-test.csv"));
        model.getSortedCampers();

        for (Camper camper : model.getCampers()) {
            System.out.println(camper.getFirstName() + " " + camper.getLastName());

            System.out.println("Classes: ");
            if (camper.getClasses().size() == 0) {
                throw new RuntimeException("class size is zero for " + camper.getFirstName() + camper.getLastName());
            }
            for (Class_ cl : camper.getClasses()) {
                System.out.print(cl.getName() + " ");
            }
            System.out.println("\n");
        }
    }
}
