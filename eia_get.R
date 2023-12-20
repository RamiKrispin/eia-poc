eia_get <- function(api_key,
                    api_path,
                    data = "value",
                    facets = NULL,
                    start = NULL,
                    end = NULL,
                    length = NULL,
                    offset = NULL,
                    frequency = NULL,
                    format = "data.frame"){
  # Error handling
  if(missing(api_key)){
    stop("The api_key argument is missing... \033[0;92m\xE2\x9D\x8C\033[0m\n")
  } else if(!is.character(api_key)){
    stop("The api_key argument is not valid... \033[0;92m\xE2\x9D\x8C\033[0m\n")
  } else if(missing(api_path)){
    stop(paste("The api_path argument is missing... \033[0;92m\xE2\x9D\x8C\033[0m\n",
               "Please check the API Dashboard for the API URL:\n",
               "https://www.eia.gov/opendata/browser/", sep = ""))
  } else if(!is.character(api_path)){
    stop(paste("The api_path argument is not valid, must be a character object \033[0;92m\xE2\x9D\x8C\033[0m\n",
               "Please check the API Dashboard for the API URL:\n",
               "https://www.eia.gov/opendata/browser/", sep = ""))
  } else if(missing(data) && !is.character(data)){
    stop("The data argument is either missing or not valid... \033[0;92m\xE2\x9D\x8C\033[0m\n")
  } else if(missing(facets) && !is.list(facets) && !is.null(facets)){
    stop("The facets argument is either missing or not valid... \033[0;92m\xE2\x9D\x8C\033[0m\n")
  } else if(!is.null(start) && !is.character(start)){
    stop(paste("The start argument is not valid... \033[0;92m\xE2\x9D\x8C\033[0m\n",
               "Please use a character using the following format:\n",
               "Date: 'YYYY-MM-DD', for example start='2022-01-01'\n",
               "Time (Hourly): 'YYYY-MM-DDTHH', for example start='2022-01-01T01'\n",sep = ""))
  } else if(!is.null(end) && !is.character(end)){
    stop(paste("The end argument is not valid... \033[0;92m\xE2\x9D\x8C\033[0m\n",
               "Please use a character using the following format:\n",
               "Date: 'YYYY-MM-DD', for example end='2022-01-01'\n",
               "Time (Hourly): 'YYYY-MM-DDTHH', for example end='2022-01-01T01'\n",sep = ""))
  } else if(!is.null(length) && !is.numeric(length) && length %% 1 != 0){
    stop(paste("The length argument is not valid: \033[0;92m\xE2\x9D\x8C\033[0m\n",
               "Must be an integer number", sep = ""))
  } else if(!is.null(offset) && !is.numeric(offset) && offset %% 1 != 0){
    stop(paste("The offset argument is not valid:\n",
               "Must be an integer number \033[0;92m\xE2\x9D\x8C\033[0m\n", sep = ""))
  } else if(!is.null(frequency) && !is.character(frequency)){
    stop(paste("The frequency argument is not valid... \033[0;92m\xE2\x9D\x8C\033[0m\n",
               "Must be a character object", sep = ""))
  } else if(format != "data.table" && format != "data.frame"){
    stop(paste("The format argument is not valid... \033[0;92m\xE2\x9D\x8C\033[0m\n",
               "Must be either 'data.frame' or 'data.table'", sep = ""))
  }

    if(substr(api_path, start = nchar(api_path), stop = nchar(api_path)) == "/"){
      api_path <- substr(api_path, start = 1, stop = nchar(api_path) - 1)
  }

  if(is.null(start)){
    s <- ""
  }  else{
    s <- paste("&start=", start, sep = "")
  }

  if(is.null(end)){
    e <- ""
  } else {
    e <- paste("&end=", end, sep = "")
  }

  f <- ""
  if(!is.null(facets)){
    for(i in names(facets)){
      for(l in facets[[i]]){
      f <- paste(f,
                 sprintf("&facets[%s][]=%s", i, l),
                 sep = "")
      }
    }
  }

  if(is.null(length)){
    l <- ""
  } else {
    l <- paste("&length=", length, sep = "")
  }

  if(is.null(offset)){
    o <- ""
  } else {
    o <- paste("&offset=", offset, sep = "")
  }

  if(is.null(frequency)){
    q <- ""
  } else {
    q <- paste("&frequency=", frequency, sep = "")
  }

  api_url <- paste("https://api.eia.gov/v2/", api_path, sep = "")
  query <- NULL
  query <- paste("curl -g '",
                 api_url,
                 "?api_key=",
                 api_key,
                 "&data[]=",
                 data,
                 s, e, f, l, o, q,
                 "' | jq -r ' .response.data | ( .[0] | keys_unsorted | map(ascii_upcase)), (.[] | [.[]]) | @csv'",
                 sep = ""
  )


  df <- NULL

  tryCatch({
    df <- data.table::fread(cmd = query,
                            header = TRUE)},
    error = function(c) "error",
    warning = function(c) "warning",
    message = function(c) "message"
  )


  if(is.null(df)){
    stop(paste("Could not pull the data... \033[0;92m\xE2\x9D\x8C\033[0m\n",
               "Check the query parameters (e.g., api key, path, etc.) or the error log\n", sep = ""))
  }
  if(format == "data.frame"){
    df <- as.data.frame(df)
  }

  names(df) <- tolower(names(df))

  return(df)
}