# 1. Clone the repository

First thing first, clone the repository.

```
git clone https://github.com/neural-maze/realtime-phone-agents-course.git
cd realtime-phone-agents-course
```

# 2. Install uv

Instead of `pip` or `poetry`, we are using `uv` as the Python package manager. 

To install uv, simply follow this [instructions](https://docs.astral.sh/uv/getting-started/installation/). 

# 3. Install the project dependencies

Once uv is intalled, you can install the project dependencies. First of all, let's create a virtual environment.

```bash
uv venv .venv
. .venv/bin/activate # or source .venv/bin/activate
uv pip install -e .
```

Just to make sure that everything is working, simply run the following command:

```bash
 uv run python --version
```

# 4. Environment Variables

Now that all the dependencies are installed, it's time to populate the `.env` file with the correct values.
To help you with this, we have created a `.env.example` file that you can use as a template.

```
cp .env.example .env
```

Now, you can open the `.env` file with your favorite text editor and set the correct values for the variables.
Right now, you'll see the following variables to be set:

```
GROQ_API_KEY=YOUR_GROQ_KEY_GOES_HERE
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL=openai/gpt-oss-20b
```

We provide support for Groq out of the box, but you can add additional providers if you extend the repository with your own fork.

> 🛠️ Or just open a PR if you think more people would benefit from this!

We selected `gpt-oss-20b` because it's one of Groq's "production" models and offered solid response quality along with fast token generation. You're free to use any model you prefer, of course.

Just keep in mind: if you opt for slower, heavy-reasoning models, the call experience may suffer.

Consider this your warning! 🤣

### Groq

To create the GROQ_API_KEY, and be able to interact with Groq models, you just need to follow this [instructions](https://console.groq.com/docs/quickstart).

![alt text](img/groq_api_key.png)

Once you have created the API key, you can copy it and paste it into an `.env` file (following the same format as the `.env.example` file).

As for the `GROQ__BASE_URL` and the `GROQ__MODEL`, you can leave the defaults from the `.env.example`.

### OpenAI

To leverage Superlinked's natural queries, we'll make use of OpenAI models (in particular, `gpt-4o-mini`).

Simply add your OpenAI API Key to the `OPENAI__API_KEY` var in your `.env` file.


### Together AI (for using Orpheus 3B through Together)

If you prefer using [Together AI](https://www.together.ai/)'s hosted version of Orpheus 3B, you will need to create an API key in your Together dashboard.

Simply add your Together AI API Key to the `TOGETHER__API_KEY` var in your `.env` file.

```
TOGETHER__API_KEY=YOUR_TOGETHER_API_KEY
```

This allows you to call the original Orpheus 3B model exactly as released by Canopy Labs.

### Runpod (for hosting your own faster-whisper and Orpheus 3B)

Since we will deploy our **own STT and TTS models** on [Runpod](https://runpod.io/), you must also create a Runpod account and generate an API key.

Simply add your Runpod API Key to the `RUNPOD__API_KEY` var in your `.env` file.

```
RUNPOD__API_KEY=YOUR_RUNPOD_API_KEY
```

Once your faster-whisper and Orpheus 3B pods are running, copy each Pod’s URL and set them in your .env file:

```
FASTER_WHISPER__API_URL=THE_URL_OF_YOUR_FASTER_WHISPER_POD
ORPHEUS__API_URL=THE_URL_OF_YOUR_ORPHEUS_POD
````

These variables allow your local Gradio application and backend to communicate directly with your hosted models on Runpod.

All other `ORPHEUS__` and `FASTER_WHISPER__` variables can be left at their defaults unless you wish to customize behavior.

### Qdrant Cloud

To use Qdrant Cloud, you need to create an account and create a cluster.

Simply add your Qdrant Cloud API Key, Cluster URL and Cluster Name to the `QDRANT__API_KEY`, `QDRANT__CLUSTER_URL` and `QDRANT__CLUSTER_NAME` vars in your `.env` file.

```
QDRANT__API_KEY=YOUR_QDRANT_CLOUD_API_KEY
QDRANT__CLUSTER_URL=YOUR_QDRANT_CLOUD_CLUSTER_URL
```

### Opik

To use Opik, you need to create an account and create a project.

Simply add your Opik API Key and Project Name to the `OPIK__API_KEY`.

### Twilio

Simply add your Twilio Account SID and Auth Token to the `TWILIO__ACCOUNT_SID` and `TWILIO__AUTH_TOKEN` vars in your `.env` file.

```
TWILIO__ACCOUNT_SID=YOUR_TWILIO_ACCOUNT_SID
TWILIO__AUTH_TOKEN=YOUR_TWILIO_AUTH_TOKEN
```

Leave `TELEPHONY__PROVIDER=twilio` when you want outbound calls to use Twilio.

### Telnyx

For Telnyx, create a TeXML Application and add the Telnyx credentials to your `.env` file:

```
TELEPHONY__PROVIDER=telnyx
TELNYX__API_KEY=YOUR_TELNYX_API_KEY
TELNYX__ACCOUNT_SID=YOUR_TELNYX_ACCOUNT_SID
TELNYX__APPLICATION_SID=YOUR_TELNYX_TEXML_APPLICATION_SID
TELNYX__WEBHOOK_PATH=/call/telnyx/events
```

The Telnyx outbound path uses the TeXML REST API and points Telnyx at:

```
https://your-public-url/voice/telephone/incoming
```

That endpoint returns the existing `<Connect><Stream>` instructions used by the FastRTC telephone handler.


# 5. Telephony

You can hook up a Stream to a provider like Twilio or Telnyx, which lets you give your app its own phone number.

[Sign up on Twilio](https://www.twilio.com/) and buy a phone number with voice support. If you’re on a trial account, you'll receive a free phone number (that's what we've done for our experiments).

For Telnyx, create a TeXML Application and set its XML request URL to your public `/voice/telephone/incoming` endpoint.


# 6. Ngrok

For local development, you’ll need a public HTTPS URL so your provider can reach your API. Since your FastAPI server is running on your machine, providers can't access it directly, which is why we use [ngrok](https://ngrok.com/).

Go to [ngrok's website](https://ngrok.com/), sign up, and grab your auth token. You'll need it to run ngrok without restrictions.

After installing ngrok and adding your auth token, expose your local server with:

```
ngrok http <port>
```

Don't worry about this, as we have a `Makefile` command to expose the correct port when the time comes. We'll cover this in the course too.
