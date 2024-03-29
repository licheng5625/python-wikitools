#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zlib.h>
#include <curl/curl.h>
#include <glib.h>

// arg1 = datafile
// arg2 = list of titles
// arg3 = redirect/title pairs

int main ( int argc, char * argv[] ) {
	curl_global_init( CURL_GLOBAL_NOTHING );
	CURL *curlob = curl_easy_init();
	char *title, *hits, *content, *res, *line, **arr, **bits;
	int hit = 0, i = 0;
	unsigned int tlen;
	void *table;
	FILE *pagelist, *redirlist;
	table = g_hash_table_new( g_str_hash, g_str_equal );
	pagelist = fopen( argv[2], "rb" );
	while(1) {
		line = malloc(256*sizeof(char));
		line = fgets( line, 256, pagelist );
		if (line == NULL) {
			break;
		}
		line = strtok( line, "\n");
		g_hash_table_insert( table, line, "");
	}
	fclose( pagelist );
	redirlist = fopen( argv[3], "rb" );
	while(1) {
		line = malloc(512*sizeof(char));
		line = fgets( line, 512, redirlist );
		if (line == NULL) {
			break;
		}
		line = strtok( line, "\n");
		arr = g_strsplit( line, "|", 2);
		g_hash_table_insert( table, arr[0], arr[1]);
		free(line);
	}
	fclose( redirlist );
	gzFile datafile;
	datafile = gzopen( argv[1], "r" );
	while(1) {
		content = malloc(2000*sizeof(char));
		content = gzgets( datafile, content, 2000 );
		if (content == Z_NULL) {
			break;
		}
		if ( !g_str_has_prefix(content, "en ") ) {
			free(content);
			if (hit == 1) {
				break;
			}
			continue;
		}
		hit = 1;
		bits = g_strsplit(content, " ", 0);
		title = bits[1];
		hits = bits[2];
		title = curl_easy_unescape( curlob, title, 0, NULL );
		if ( strchr( title, ' ' ) ) {
			tlen = strlen(title);
			for (i=0; i<tlen; i++) {
				if( title[i] == ' ') {
					title[i] = '_';
				}
			}
		}
		res = g_hash_table_lookup( table, title );
		if ( res == "" ) {
			printf(title);
		} 
		if(res != NULL) {
			if (res != "") {
				printf(res);
			}
			printf(" | %s\n", hits);
		}
		g_strfreev(bits);
		free(content);
		curl_free(title);
	}
	curl_easy_cleanup( curlob );
	curl_global_cleanup();
	return 0;
}
