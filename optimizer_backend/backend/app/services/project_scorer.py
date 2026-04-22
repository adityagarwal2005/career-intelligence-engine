import json
from typing import List, Dict, Any
from pathlib import Path


class ProjectScorer:
    """Score projects from dataset against job description using keyword overlap."""
    
    def __init__(self, dataset_path: str = "data/projects_dataset.json"):
        """Initialize scorer with projects dataset."""
        self.dataset_path = Path(dataset_path)
        self.projects = self._load_projects()
    
    def _load_projects(self) -> List[Dict[str, Any]]:
        """Load projects from JSON dataset."""
        if not self.dataset_path.exists():
            return []
        
        with open(self.dataset_path, "r") as f:
            return json.load(f)
    
    def score_projects(self, job_description: str) -> List[Dict[str, Any]]:
        """
        Score all projects against JD and return top 4 with scores.
        
        Scoring logic:
        - Required skills match: +4 points
        - Tools/tech stack match: +3 points
        - Keywords match: +2 points
        - Domain match: +2 points
        
        Args:
            job_description: Job description text to score against
            
        Returns:
            List of top 4 projects with scores, sorted by score descending
        """
        jd_lower = job_description.lower()
        scored_projects = []
        
        for project in self.projects:
            score = 0
            matched_criteria = []
            
            # Score required skills (4 points each)
            for skill in project.get("required_skills", []):
                if skill.lower() in jd_lower:
                    score += 4
                    matched_criteria.append(f"skill:{skill}")
            
            # Score tools/tech stack (3 points each)
            for tool in project.get("tech_stack", []):
                if tool.lower() in jd_lower:
                    score += 3
                    matched_criteria.append(f"tool:{tool}")
            
            # Score keywords (2 points each)
            for keyword in project.get("keywords", []):
                if keyword.lower() in jd_lower:
                    score += 2
                    matched_criteria.append(f"keyword:{keyword}")
            
            # Score domain (2 points each)
            for domain in project.get("domain", []):
                if domain.lower() in jd_lower:
                    score += 2
                    matched_criteria.append(f"domain:{domain}")
            
            scored_projects.append({
                "score": score,
                "matched_criteria": matched_criteria,
                "project": project
            })
        
        # Sort by score descending and return top 4
        scored_projects.sort(key=lambda x: x["score"], reverse=True)
        return scored_projects[:4]
    
    def get_projects_for_optimizer(self, job_description: str) -> List[Dict[str, Any]]:
        """
        Get top 4 projects formatted for optimizer service.
        
        Returns only the project data (without scores) for the optimizer.
        """
        scored = self.score_projects(job_description)
        return [item["project"] for item in scored]
