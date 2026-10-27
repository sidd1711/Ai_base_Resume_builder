"""
Taxonomy of skills, tools, frameworks, and job role archetypes.
Supports alias normalization (e.g. Postgres -> PostgreSQL, K8s -> Kubernetes).
"""

# Alias map: lowercase variant -> Canonical Name
SKILL_ALIASES = {
    # Databases
    'postgres': 'PostgreSQL',
    'postgresql': 'PostgreSQL',
    'psql': 'PostgreSQL',
    'mysql': 'MySQL',
    'mongo': 'MongoDB',
    'mongodb': 'MongoDB',
    'redis': 'Redis',
    'sqlite': 'SQLite',
    'sqlite3': 'SQLite',
    'cassandra': 'Cassandra',
    'oracle db': 'Oracle Database',
    'dynamodb': 'DynamoDB',

    # Languages
    'python': 'Python',
    'python3': 'Python',
    'js': 'JavaScript',
    'javascript': 'JavaScript',
    'ts': 'TypeScript',
    'typescript': 'TypeScript',
    'golang': 'Go',
    'go': 'Go',
    'c++': 'C++',
    'cpp': 'C++',
    'c#': 'C#',
    'csharp': 'C#',
    'c': 'C',
    'java': 'Java',
    'kotlin': 'Kotlin',
    'swift': 'Swift',
    'rust': 'Rust',
    'ruby': 'Ruby',
    'php': 'PHP',
    'html': 'HTML5',
    'html5': 'HTML5',
    'css': 'CSS3',
    'css3': 'CSS3',
    'sass': 'Sass',
    'sql': 'SQL',
    'bash': 'Bash/Shell',
    'shell': 'Bash/Shell',

    # Frameworks
    'django': 'Django',
    'django rest framework': 'Django REST Framework',
    'drf': 'Django REST Framework',
    'flask': 'Flask',
    'fastapi': 'FastAPI',
    'react': 'React',
    'react.js': 'React',
    'reactjs': 'React',
    'next.js': 'Next.js',
    'nextjs': 'Next.js',
    'vue': 'Vue.js',
    'vue.js': 'Vue.js',
    'vuejs': 'Vue.js',
    'angular': 'Angular',
    'angularjs': 'Angular',
    'node': 'Node.js',
    'node.js': 'Node.js',
    'nodejs': 'Node.js',
    'express': 'Express.js',
    'express.js': 'Express.js',
    'spring': 'Spring Boot',
    'spring boot': 'Spring Boot',
    'laravel': 'Laravel',
    'asp.net': 'ASP.NET',
    '.net': '.NET',
    'dotnet': '.NET',
    'bootstrap': 'Bootstrap',
    'tailwind': 'Tailwind CSS',
    'tailwind css': 'Tailwind CSS',

    # Cloud & DevOps
    'aws': 'AWS',
    'amazon web services': 'AWS',
    'azure': 'Azure',
    'microsoft azure': 'Azure',
    'gcp': 'Google Cloud Platform',
    'google cloud': 'Google Cloud Platform',
    'docker': 'Docker',
    'k8s': 'Kubernetes',
    'kubernetes': 'Kubernetes',
    'git': 'Git',
    'github': 'GitHub',
    'gitlab': 'GitLab',
    'ci/cd': 'CI/CD',
    'jenkins': 'Jenkins',
    'linux': 'Linux',
    'nginx': 'Nginx',
    'terraform': 'Terraform',
    'ansible': 'Ansible',
    'graphql': 'GraphQL',
    'rest': 'REST APIs',
    'rest api': 'REST APIs',
    'restful': 'REST APIs',
    'microservices': 'Microservices',

    # AI / ML / Data
    'pytorch': 'PyTorch',
    'tensorflow': 'TensorFlow',
    'scikit-learn': 'scikit-learn',
    'sklearn': 'scikit-learn',
    'pandas': 'Pandas',
    'numpy': 'NumPy',
    'matplotlib': 'Matplotlib',
    'seaborn': 'Seaborn',
    'tableau': 'Tableau',
    'power bi': 'Power BI',
    'powerbi': 'Power BI',
    'nlp': 'NLP',
    'natural language processing': 'NLP',
    'computer vision': 'Computer Vision',
    'opencv': 'OpenCV',
    'llm': 'LLMs',
    'large language models': 'LLMs',

    # Soft skills & Methodologies
    'agile': 'Agile',
    'scrum': 'Scrum',
    'jira': 'Jira',
    'problem solving': 'Problem Solving',
    'communication': 'Communication',
    'teamwork': 'Teamwork',
    'leadership': 'Leadership',
    'critical thinking': 'Critical Thinking',
}

# Standard archetype skills for the searchable Job Role Selector
JOB_ROLE_PRESETS = {
    'Python Developer': {
        'required': ['Python', 'Django', 'REST APIs', 'SQL', 'Git'],
        'preferred': ['PostgreSQL', 'Docker', 'FastAPI', 'Redis', 'AWS', 'CI/CD', 'Linux'],
        'summary': 'Develop backend services, design robust APIs, and manage database integrations using Python and Django.'
    },
    'Django Developer': {
        'required': ['Django', 'Python', 'PostgreSQL', 'REST APIs', 'Git'],
        'preferred': ['Django REST Framework', 'Redis', 'Celery', 'Docker', 'HTML5', 'CSS3', 'JavaScript'],
        'summary': 'Build scalable full-stack web applications and microservices using Django and modern web standards.'
    },
    'Frontend Developer': {
        'required': ['JavaScript', 'HTML5', 'CSS3', 'React', 'Git'],
        'preferred': ['TypeScript', 'Next.js', 'Redux', 'Tailwind CSS', 'REST APIs', 'Bootstrap'],
        'summary': 'Create responsive, accessible, high-performance web user interfaces.'
    },
    'Backend Developer': {
        'required': ['Python', 'REST APIs', 'SQL', 'Git', 'Linux'],
        'preferred': ['PostgreSQL', 'Docker', 'Redis', 'Microservices', 'Kubernetes', 'AWS'],
        'summary': 'Architect secure server-side logic, high-throughput microservices, and reliable database architectures.'
    },
    'Full-Stack Developer': {
        'required': ['JavaScript', 'Python', 'React', 'Django', 'SQL', 'Git'],
        'preferred': ['TypeScript', 'PostgreSQL', 'Docker', 'REST APIs', 'AWS', 'Tailwind CSS'],
        'summary': 'Design and maintain end-to-end web applications across client interfaces and backend architectures.'
    },
    'Data Analyst': {
        'required': ['SQL', 'Python', 'Pandas', 'NumPy', 'Tableau'],
        'preferred': ['Power BI', 'Excel', 'Matplotlib', 'Statistics', 'Data Visualization'],
        'summary': 'Extract, transform, and analyze complex datasets to uncover strategic business insights.'
    },
    'Data Scientist': {
        'required': ['Python', 'scikit-learn', 'SQL', 'Pandas', 'Statistics'],
        'preferred': ['PyTorch', 'TensorFlow', 'NLP', 'Docker', 'AWS', 'Tableau'],
        'summary': 'Build predictive machine learning models, run statistical experiments, and deliver data products.'
    },
    'Machine Learning Engineer': {
        'required': ['Python', 'PyTorch', 'scikit-learn', 'Docker', 'Git'],
        'preferred': ['TensorFlow', 'Kubernetes', 'AWS', 'LLMs', 'MLOps', 'FastAPI'],
        'summary': 'Deploy, optimize, and maintain production-grade machine learning pipelines and inference services.'
    },
    'DevOps Engineer': {
        'required': ['Linux', 'Docker', 'Kubernetes', 'CI/CD', 'Git'],
        'preferred': ['Terraform', 'AWS', 'Ansible', 'Jenkins', 'Python', 'Bash/Shell', 'Nginx'],
        'summary': 'Automate cloud infrastructure provisioning, container orchestration, and continuous deployment.'
    },
    'UI/UX Designer': {
        'required': ['Figma', 'User Research', 'Wireframing', 'Prototyping'],
        'preferred': ['HTML5', 'CSS3', 'Design Systems', 'Usability Testing', 'Adobe XD'],
        'summary': 'Conduct user research and design intuitive, accessible user interfaces and wireframes.'
    },
    'Cybersecurity Analyst': {
        'required': ['Linux', 'Networking', 'Security Audit', 'Bash/Shell'],
        'preferred': ['Python', 'SIEM', 'Penetration Testing', 'Firewalls', 'Incident Response'],
        'summary': 'Monitor systems for security breaches, execute vulnerability assessments, and safeguard network assets.'
    },
    'Business Analyst': {
        'required': ['Requirements Gathering', 'SQL', 'Agile', 'Jira'],
        'preferred': ['Tableau', 'Power BI', 'Data Modeling', 'Communication', 'Scrum'],
        'summary': 'Bridge business requirements with engineering teams through detailed specifications and data modeling.'
    }
}
