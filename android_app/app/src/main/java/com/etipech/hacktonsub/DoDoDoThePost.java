package com.etipech.hacktonsub;

import android.net.Uri;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;

public class DoDoDoThePost extends AppCompatActivity {

    NetworkAsyncTask nwAsync;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_do_do_do_the_post);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        TextView textView = findViewById(R.id.textView);
        String res;

        nwAsync = new NetworkAsyncTask();
        Bundle b = getIntent().getExtras();
        String email = b.getString("email");
        String storeNumber = b.getString("storeNumber");
        String mark = b.getString("mark");
        String ticket = b.getString("ticket");

        System.out.println(email);
        System.out.println(storeNumber);
        System.out.println(mark);
        System.out.println(ticket);

        try {
            res = nwAsync.execute(email, storeNumber, mark, ticket).get();
            textView.setText(res);
        }catch (Exception e) {
            //TODO
        }

    }
}
