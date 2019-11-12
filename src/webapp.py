#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Emmanuel Raj
"""

import pickle
from flask import Flask, request
import json
import os
import numpy as np
import tensorflow as tf
from flasgger import Swagger
from time import time

import model, sample, encoder


app = Flask(__name__)
swagger = Swagger(app)

@app.route('/text-generate')
def inference_gpt2(
    model_name='',
    seed=None,
    nsamples=1,
    batch_size=1,
    length=None,
    temperature=1,
    top_k=0,
    top_p=1,
    models_dir='models',
    text = None
):
    """Endpoints takes input text to generate text out of it.
    ---
    parameters:
      - name: input_text
        in: query
        type: number
        required: true
      - name: model_name
        in: query
        type: string
        enum: ['124M', '355M', '774M', '1558M']
        required: true
        default: all         
      
    """
    input_text = request.args.get("input_text")
    model_name = request.args.get("model_name")
    

    models_dir = os.path.expanduser(os.path.expandvars(models_dir))
    if batch_size is None:
        batch_size = 1
    assert nsamples % batch_size == 0

    enc = encoder.get_encoder(model_name, models_dir)
    hparams = model.default_hparams()
    with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    if length is None:
        length = hparams.n_ctx // 2
    elif length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

    with tf.Session(graph=tf.Graph()) as sess:
        context = tf.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        output = sample.sample_sequence(
            hparams=hparams, length=length,
            context=context,
            batch_size=batch_size,
            temperature=temperature, top_k=top_k, top_p=top_p
        )

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
        saver.restore(sess, ckpt)


        raw_text = text
        context_tokens = enc.encode(raw_text)        
        generated = 0
        for _ in range(nsamples // batch_size):
            out = sess.run(output, feed_dict={
            context: [context_tokens for _ in range(batch_size)]
            })[:, len(context_tokens):]
        for i in range(batch_size):
            generated += 1
            text = enc.decode(out[i])
            print("=" * 40 + " SAMPLE " + str(generated) + " " + "=" * 40)
            print(text)
        print("=" * 80)

        output = text

    
        
    start = time()
    inference_gpt2()
    elapsed = time() - start
    print('Inference time: {}'.format(elapsed))

    
    return output

    


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
