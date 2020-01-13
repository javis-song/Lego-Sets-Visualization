package edu.gatech.cse6242;
import java.io.IOException;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Q4 {

  public static class Mapper1
       extends Mapper<Object, Text, IntWritable, IntWritable>{

    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
    	String[] sa = value.toString().split("\t");
    	context.write(new IntWritable(Integer.parseInt(sa[0])), new IntWritable(1));
      context.write(new IntWritable(Integer.parseInt(sa[1])), new IntWritable(-1));
    }
  }

  public static class Reducer1
       extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {

    public void reduce(IntWritable key, Iterable<IntWritable> values,
                       Context context
                       ) throws IOException, InterruptedException {
      int sum = 0;
      for (IntWritable val : values) {
          sum += val.get();
      }
      context.write(key, new IntWritable(sum));
    }
  }

  public static class Mapper2
       extends Mapper<Object, Text, IntWritable, IntWritable>{

    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      String[] sa = value.toString().split("\t");
      context.write(new IntWritable(Integer.parseInt(sa[1])), new IntWritable(1));
    }
  }

  public static class Reducer2
       extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {

    public void reduce(IntWritable key, Iterable<IntWritable> values,
                       Context context
                       ) throws IOException, InterruptedException {
      int sum = 0;
      for (IntWritable val : values) {
          sum += val.get();
      }
      context.write(key, new IntWritable(sum));
    }
  }

  public static void main(String[] args) throws Exception {
      Path out = new Path(args[1]);
      Configuration conf1 = new Configuration();
      Job j1 = Job.getInstance(conf1, "Q4");
      j1.setJarByClass(Q4.class);
      j1.setMapperClass(Mapper1.class);
      j1.setReducerClass(Reducer1.class);
      j1.setMapOutputKeyClass(IntWritable.class);
      j1.setMapOutputValueClass(IntWritable.class);
      j1.setOutputKeyClass(IntWritable.class);
      j1.setOutputValueClass(IntWritable.class);

      FileInputFormat.addInputPath(j1, new Path(args[0]));
      FileOutputFormat.setOutputPath(j1, new Path(out,"out1"));
      j1.waitForCompletion(true);

      Configuration conf2 = new Configuration();
      Job j2 = Job.getInstance(conf2, "Q4");
      j2.setJarByClass(Q4.class);
      j2.setMapperClass(Mapper2.class);
      j2.setReducerClass(Reducer2.class);
      j2.setMapOutputKeyClass(IntWritable.class);
      j2.setMapOutputValueClass(IntWritable.class);
      j2.setOutputKeyClass(IntWritable.class);
      j2.setOutputValueClass(IntWritable.class);

      FileInputFormat.addInputPath(j2, new Path(out,"out1"));
      FileOutputFormat.setOutputPath(j2, new Path(out,"out2"));
      System.exit(j2.waitForCompletion(true) ? 0 : 1);
  }
}
