from models import Skill

keywords = ["python", "javascript", "html", "css", "ruby", "bash",
               "linux", "unix", "rest", "restful", "api", "aws",
               "cloud", "svn", "git", "junit", "testng", "java", "php",
               "agile", "scrum", "nosql", "mysql", "postgresdb", "postgres",
               "shell", "scripting", "mongodb", "puppet", "chef", "ansible",
               "nagios", "sumo", "nginx", "haproxy", "docker", "automation",
               "jvm", "scikit-learn", "tensorflow", "vue", "react", "angular",
               "webpack", "drupal", "gulp", "es6", "jquery", "sass", "scss",
               "less", "nodejs", "node.js", "graphql", "postgresql", "db2",
               "sql", "spring", "microservices", "kubernates", "swagger",
               "hadoop", "ci/cd", "django", "elasticsearch", "redis", "c++",
               "c", "hive", "spark", "apache", "mesos", "gcp", "jenkins",
               "azure", "allcloud", "amqp", "gcp", "objective-c", "kotlin"
               "kafka", "jira", "cassandra", "containers", "oop", "redis",
               "memcached", "redux", "bigquery", "bigtable", "hbase", "ec2",
               "s3", "gradle", ".net", "riak", "shell", "hudson", "maven",
               "j2ee", "oracle", "swarm", "sysbase", "dynamodb", "neo4",
               "allcloud", "grunt", "gulp", "apex", "rails", "mongo", "apis",
               "html5", "css3", "rails", "scala", "rasa", "soa", "soap",
               "microservices", "storm", "flink", "gitlab", "ajax",
               "micro-services", "oop", "saas", "struts", "jsp", "freemarker",
               "hibernate", "rlak", "solidity", "heroku", "ecs", "gce",
               "scripting", "perl", "c#", "golang", "xml", "newrelic",
               "grafana", "helm", "polymer", "closure", "backbone",
               "atlassian", "angularjs", "flask", "scikitlearn", "theano",
               "numpy", "scipy", "panda", "tableau", "gensim", "rpc",
               "graphql", "iaas", "paas", "azure", "es", "solr", "http", "iot",
               "kinesis", "lambda", "typescript", "gradle", "buck", "bazel"]
for skill in keywords:
    new_skill = Skill(name=skill)
    new_skill.save()
