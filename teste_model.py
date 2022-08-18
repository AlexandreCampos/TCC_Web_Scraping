from model.database import *
import pprint

# create_table(
# 	"""
# 	    CREATE TABLE store_config (
# 	        id INT AUTO_INCREMENT PRIMARY KEY,
# 	        name VARCHAR(255),
# 	        url_base VARCHAR(255)
# 	    )
# 	"""
# )

# insert(
# 	"""
# 	    INSERT INTO store_config
# 	        (name, url_base)
# 	    VALUES
# 	        ('JOAO2', 'aaa2@aaa.com'),
# 	        ('MARIA2', 'bbb2@aaa.com')
# 	"""	
# )

# update(
# 	"""
# 	    UPDATE store_config
# 	    SET name = "MARIA2"
# 	    WHERE id = 6
# 	"""	
# )

# delete(
# 	"""
# 	    DELETE
# 	   	FROM store_config
# 	   	WHERE id = 8
# 	"""	
# )

# result = select(
# 	"""
# 	    SELECT *
# 	    FROM store_config
# 	"""
# )

# pprint.pprint(result)

result = table_exists("category")
import pdb; pdb.set_trace()
