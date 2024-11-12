# Zania Assignment

This is a simple FastAPI application that allows users to upload PDF and JSON files and receive answers from a language model.

## Usage

### Prerequisites

This project uses `uv` for python version management and package management. After you install `uv`, you can use the following command to install the required packages:

```bash
uv install
```

### Environment Variables

You will need to set the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key.

or you can create a `.env` file in the root directory of the project and add the following line:

```
OPENAI_API_KEY=your_api_key
```


### Start server

To start the server, you can use the following command:
```
uv shell
fastapi run
```

This will start the server on port 8000.

### Uploading Files

Both doc and question file key are required.

To upload a PDF file, you can use the following command:

```bash
curl -X POST -F "doc=@path/to/file.pdf" -F "question=@path/to/file.json" http://localhost:8000/upload
```

### Doc file format

```json
{
  "docs": [
    {
      "page_content": "Hello world",
      "metadata": {"source": "test.pdf"}
    },
    {
      "page_content": "User must use digital MFA or any hardware MFA device to access the account",
      "metadata": {"source": "test.pdf"}
    }
  ]
}
```

### Question file format

```json
{
  "questions": [
    "hello",
    "can user access account with MFA"
  ]
}
```

