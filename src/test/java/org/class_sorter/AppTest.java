package org.class_sorter;

import static org.junit.Assert.assertTrue;

import org.class_sorter.model.Camper;
import org.class_sorter.model.CamperImpl;
import org.class_sorter.model.ClassImpl;
import org.class_sorter.model.Class_;
import org.junit.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Unit test for simple App.
 */
public class AppTest {
    @Test
    public void shouldAnswerWithTrue()
    {
        assertTrue( true );
    }

    @Test
    public void test() {

        List<Class_> classes = new ArrayList<>();
        Class_ paintball = new ClassImpl("Paintball",10,true);
        Class_ horses = new ClassImpl("Horse Back Riding",15,false);
        Class_ kayaking = new ClassImpl("Kayaking", 15, false);
        Class_ drama = new ClassImpl("Drama",12,false);
        Class_ rifles = new ClassImpl("Rifles", 12, true);
        Class_ shotguns = new ClassImpl("FiveStand",10,true);
        Class_ photography = new ClassImpl("Photography", 10, false);
        Class_ climbing = new ClassImpl("Climbing", 15, false);
        Class_ fishing = new ClassImpl("Fishing", 5, false);
        Class_ archery = new ClassImpl("Archery", 9, false);
        Class_ sports = new ClassImpl("Sports", 13,false);

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

        List<Class_> pref1 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            int n = (int) (Math.random() * (10));
            if (!pref1.contains(classes.get(n))) {
                pref1.add(classes.get(n));
            }else {
                i--;
            }
        }

        List<Class_> pref2 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            int n = (int) (Math.random() * (10));
            if (!pref2.contains(classes.get(n))) {
                pref2.add(classes.get(n));
            }else {
                i--;
            }
        }
        List<Class_> pref3 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            int n = (int) (Math.random() * (10));
            if (!pref3.contains(classes.get(n))) {
                pref3.add(classes.get(n));
            }else {
                i--;
            }
        }
        List<Class_> pref4 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            int n = (int) (Math.random() * (10));
            if (!pref4.contains(classes.get(n))) {
                pref4.add(classes.get(n));
            }else {
                i--;
            }
        }
        List<Class_> pref5 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            int n = (int) (Math.random() * (10));
            if (!pref5.contains(classes.get(n))) {
                pref5.add(classes.get(n));
            }else {
                i--;
            }
        }
        List<Class_> pref6 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            int n = (int) (Math.random() * (10));
            if (!pref6.contains(classes.get(n))) {
                pref6.add(classes.get(n));
            }else {
                i--;
            }
        }
        List<Class_> pref7 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            int n = (int) (Math.random() * (10));
            if (!pref7.contains(classes.get(n))) {
                pref7.add(classes.get(n));
            }else {
                i--;
            }
        }
        List<Class_> pref8 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            int n = (int) (Math.random() * (10));
            if (!pref8.contains(classes.get(n))) {
                pref8.add(classes.get(n));
            }else {
                i--;
            }
        }

        List<List<Class_>> preferences = new ArrayList<>();
        preferences.add(pref1);
        preferences.add(pref2);
        preferences.add(pref3);
        preferences.add(pref4);
        preferences.add(pref5);
        preferences.add(pref6);
        preferences.add(pref7);
        preferences.add(pref8);


        Camper charlie = new CamperImpl("Charlie","4L",12,true,pref1);
        Camper Mack = new CamperImpl("Mack","3L",14,true,pref3);
        Camper Lizzie = new CamperImpl("Lizzie","3",9,false,pref5);
        Camper Ellie = new CamperImpl("Ellie","1",15,true,pref7);
        Camper Chase = new CamperImpl("Chase","Chase",7,false,pref8);
        Camper Nick = new CamperImpl("Nick","13",13,true,pref2);
        Camper John = new CamperImpl("John","11",12,true,pref3);
        Camper Nathan = new CamperImpl("Nathan","11",12,true,pref4);
        Camper Marissa = new CamperImpl("Marissa","12",10,true,pref7);
        Camper Sherry = new CamperImpl("Sherry","14",14,true,pref5);
        Camper Carlos = new CamperImpl("Carlos","7",9,true,pref3);
        Camper Haley = new CamperImpl("Haley","6",10,true,pref1);
        Camper Patrick = new CamperImpl("Patrick","11",12,true,pref6);



    }
}
