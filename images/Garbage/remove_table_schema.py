import sys
import re

"""
Example input:
CREATE TABLE public.item (
    i_id integer NOT NULL,
    title character varying(128) NOT NULL,
    description character varying(512) DEFAULT NULL::character varying,
    creation_date timestamp without time zone
);
ALTER TABLE ONLY public.review
    ADD CONSTRAINT review_i_id_fkey FOREIGN KEY (i_id) REFERENCES public.item(i_id) ON DELETE CASCADE;
....

Example output:
CREATE TABLE item (
    i_id integer NOT NULL,
    title character varying(128) NOT NULL,
    description character varying(512) DEFAULT NULL::character varying,
    creation_date timestamp without time zone
);
ALTER TABLE ONLY review
    ADD CONSTRAINT review_i_id_fkey FOREIGN KEY (i_id) REFERENCES public.item(i_id) ON DELETE CASCADE;
"""
def remove_table_schema(ddl):
    # traverse line by line
    lines = ddl.splitlines()
    output = ""
    for line in lines:
        if line.startswith("CREATE TABLE") or line.startswith("ALTER TABLE"):
            # remove schema name
            line = re.sub('[^ ]+\.', '', line)
        output += f"{line}\n"
    return output

if __name__ == "__main__":
    ddl_filename = sys.argv[1]
    ddl_output_filename = sys.argv[2]
    with open(ddl_filename, "r") as fp:
        ddl = fp.read()
        ddl = remove_table_schema(ddl)
    with open(ddl_output_filename, "w") as fp:
        fp.write(ddl)
