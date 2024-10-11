from typing import Any, Dict, List, Optional, Union

import lamini
from lamini.api.lamini_config import get_config, get_configured_key, get_configured_url
from lamini.api.rest_requests import make_async_web_request


class BatchEmbeddings:
    """Handler for formatting and POST request for the batch submission API

    Parameters
    ----------
    api_key: Optional[str]
        Lamini platform API key, if not provided the key stored
        within ~.lamini/configure.yaml will be used. If either
        don't exist then an error is raised.

    api_url: Optional[str]
        Lamini platform api url, only needed if a different url is needed outside of the
        defined ones here: https://github.com/lamini-ai/lamini-platform/blob/main/sdk/lamini/api/lamini_config.py#L68
            i.e. localhost, staging.lamini.ai, or api.lamini.ai
            Additionally, LLAMA_ENVIRONMENT can be set as an environment variable
            that will be grabbed for the url before any of the above defaults

    """

    def __init__(
        self,
        client,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
    ) -> None:
        """
        Configuration dictionary for platform metadata provided by the following function:
                https://github.com/lamini-ai/lamini-platform/blob/main/sdk/lamini/api/lamini_config.py
            Configurations currently hold the following keys and data as a yaml format:
                local:
                    url: <url>
                staging:
                    url: <url>
                production:
                    url: <url>

                local:
                    key: <auth-key>
                staging:
                    key: <auth-key>
                production:
                    key:
                        <auth-key>
        """
        self.config = get_config()
        self.client = client
        self.api_key = api_key or lamini.api_key or get_configured_key(self.config)
        self.api_url = api_url or lamini.api_url or get_configured_url(self.config)
        self.api_prefix = self.api_url + "/v1/"

    async def submit(
        self,
        prompt: Union[str, List[str]],
        model_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Handles construction of the POST request headers and body, then
        a web request is made with the response returned.

        Parameters
        ----------
        prompt: Union[str, List[str]]:
            Input prompt for the LLM

        model_name: str
            LLM model name from HuggingFace

        Returns
        -------
        resp: Dict[str, Any]
            Json data returned from POST request
        """
        req_data = self.make_llm_req_map(
            prompt=prompt,
            model_name=model_name,
        )
        resp = await make_async_web_request(
            self.client,
            self.api_key,
            self.api_prefix + "batch_embeddings",
            "post",
            req_data,
        )
        return resp

    async def check_result(
        self,
        id: str,
    ) -> Dict[str, Any]:
        """Check for the result of a batch request with the appropriate batch id."""
        resp = await make_async_web_request(
            self.client,
            self.api_key,
            self.api_prefix + f"batch_embeddings/{id}/result",
            "get",
        )
        return resp

    def make_llm_req_map(
        self,
        model_name: Optional[str],
        prompt: Union[str, List[str]],
    ) -> Dict[str, Any]:
        """Returns a dict of parameters for calling the remote LLM inference API.

        NOTE: Copied from lamini.py.

        TODO: Create a helper function that accepts all values and returns a dict. And replace callers
        of self.make_llm_req_map() with the calling of the free function.

        Parameters
        ----------
        model_name: str
            LLM model name from HuggingFace

        prompt: Union[str, List[str]]:
            Input prompt for the LLM

        Returns
        -------
        req_data: Dict[str, Any]
            Constructed dictionary with parameters provided into the correctly
            specified keys for a REST request.
        """

        req_data = {}
        if model_name is not None:
            req_data["model_name"] = model_name
        req_data["prompt"] = prompt
        return req_data
