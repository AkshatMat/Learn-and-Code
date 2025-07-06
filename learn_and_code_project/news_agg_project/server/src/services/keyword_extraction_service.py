import json
import re
from typing import List, Optional
import boto3
from langchain_aws import ChatBedrock
from config.settings import settings
from utils.exception import KeywordExtractionError, ConfigurationError
from utils.logger import logger

class KeywordExtractionService:    
    def __init__(self):
        self.llm: Optional[ChatBedrock] = None
        self._initialize_llm()
    
    def _initialize_llm(self) -> None:
        try:
            if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY:
                logger.warning("AWS credentials not found. Keyword extraction will be disabled.")
                return
            
            bedrock_runtime = boto3.client(
                service_name="bedrock-runtime",
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
            
            model_kwargs = {"temperature": settings.BEDROCK_TEMPERATURE}
            
            self.llm = ChatBedrock(
                client=bedrock_runtime,
                model_id=settings.BEDROCK_MODEL_ID,
                model_kwargs=model_kwargs
            )
            
            logger.info("AWS Bedrock LLM initialized successfully")
            
        except Exception as e:
            logger.warning(f"Failed to initialize AWS Bedrock LLM: {str(e)}")
            self.llm = None
    
    def extract_keywords(self, content: str, fallback_keywords: Optional[List[str]] = None) -> List[str]:
        if not self.llm:
            logger.info("LLM not available, using fallback keywords")
            return fallback_keywords or []
        
        if not content:
            return fallback_keywords or []
        
        try:
            truncated_content = content[:2000]
            
            prompt = f"""
            Extract 5-10 relevant keywords from the following article content. 
            Return only the keywords as a JSON array, nothing else.
            
            Content: {truncated_content}
            
            Format: ["keyword1", "keyword2", "keyword3"]
            """
            
            response = self.llm.invoke(prompt)
            keywords_text = response.content.strip()
            
            keywords = self._parse_keywords_response(keywords_text)
            
            if keywords:
                logger.info(f"Successfully extracted {len(keywords)} keywords using LLM")
                return keywords
            else:
                logger.warning("LLM returned empty keywords, using fallback")
                return fallback_keywords or []
                
        except Exception as e:
            logger.error(f"Error extracting keywords with LLM: {str(e)}")
            return fallback_keywords or []
    
    def _parse_keywords_response(self, response_text: str) -> List[str]:
        try:
            keywords = json.loads(response_text)
            if isinstance(keywords, list):
                return [str(k) for k in keywords if k]
        except json.JSONDecodeError:
            pass
        
        array_match = re.search(r'\[(.*?)\]', response_text, re.DOTALL)
        if array_match:
            try:
                keywords = json.loads(f'[{array_match.group(1)}]')
                if isinstance(keywords, list):
                    return [str(k) for k in keywords if k]
            except json.JSONDecodeError:
                pass
        
        return []
    
    def is_available(self) -> bool:
        return self.llm is not None